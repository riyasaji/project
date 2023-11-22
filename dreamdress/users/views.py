
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import auth
from django.contrib.auth import login,authenticate,logout
from .models import tbl_user
from .models import UserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from django.contrib import messages

from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.utils.encoding import DjangoUnicodeDecodeError
import re

from django.views.generic import View
# from .utils import *
from .utils import TokenGenerator,generate_token

#for activating user account
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect

#email
from django.conf import settings
from django.core.mail import EmailMessage

#threading
import threading
class EmailThread(threading.Thread):
       def __init__(self, email_message):
           self.email_message=email_message
           super().__init__()
       def run(self):
              self.email_message.send()

#reset passwor generater
from django.contrib.auth.tokens import PasswordResetTokenGenerator

@login_required(login_url='signin')
def home(request):
    return render(request,'home.html') 


def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def registration(request):
    if request.method=='POST':
        username=request.POST['username']
        if tbl_user.objects.filter(username=username).exists():
            messages.success(request,'Username Already Exists')
            return redirect('registration')
        
        email=request.POST['email']
        if tbl_user.objects.filter(email=email).exists():
            messages.success(request,'Email Already Exists')
            return redirect('registration')
        
        password=request.POST['password']
        user_type = request.POST.get('user_type') 
        
        user=tbl_user(username=username,email=email,user_type=user_type)
        
        user.set_password(password)
        
        #authentication
        user.is_active=False
        user.save()
        
        current_site=get_current_site(request)  
        email_subject="Activate your account"
        message=render_to_string('activate.html',{
                   'user':user,
                   'domain':current_site.domain,
                   'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                   'token':generate_token.make_token(user)


            })

        email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email],)
        EmailThread(email_message).start()
        messages.info(request,"Active your account by clicking the link send to your email")

        if user_type == 'customer':
            messages.info(request, "Activate your account by clicking the link sent to your email")
            return redirect('signin')
        elif user_type == 'seller':
            # Create Seller instance if the user is a seller
            Seller.objects.create(user=user)
            # Redirect seller to seller update page
            messages.info(request, "Activate your account by clicking the link sent to your email")
            return redirect('seller_registeration')
    else:
        return render(request,'registration.html')

def signin(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username, password=password)
        if user is not None:
            if user.is_active:
                if user.is_superuser:
                    return redirect('dashboard')
                if user.user_type == 'seller':
                    seller = Seller.objects.get(user=user)
                    if seller.is_approved:  # Check if the seller is approved by admin
                        login(request, user)
                        return redirect('seller_dashboard')
                    else:
                        messages.error(request, 'Your account is pending approval by the admin.')
                        return redirect('signin')
                else:
                        login(request, user)
                        return redirect('home')
            else:
                messages.error(request, 'Your account is not active.')
                return redirect('signin')
        else:
            messages.error(request,'Email and Password Invalid')
            return redirect('signin')

    return render(request,'signin.html')

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('signin')

class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_str(urlsafe_base64_decode(uidb64))
            user=tbl_user.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.info(request,"Account activated sucessfully")
            return redirect('signin')
        return render(request,"auth/activatefail.html")
    

def check_username(request):
    username = request.GET.get('username','')
    print(username)
    user_exists = tbl_user.objects.filter(username=username).exists()
    return JsonResponse({'exists': user_exists})

def check_email(request):
    email= request.GET.get('email','')
    email_exists = tbl_user.objects.filter(email=email).exists()
    return JsonResponse({'exists': email_exists})


def dashboard(request):
    recent_users = tbl_user.objects.all().filter(is_superuser=False).order_by('-last_login')[:10]
    return render(request,'dashboard.html', {'recent_users': recent_users})

def customer_list(request):
    customers = tbl_user.objects.filter(user_type='customer')  # Fetch customers
    return render(request, 'customerList_admin.html', {'customers': customers})

def seller_list(request):
    sellers = tbl_user.objects.filter(user_type='seller')  # Fetch sellers
    return render(request, 'sellerList_admin.html', {'sellers': sellers})

def seller_count_view(request):
    sellers_count = Seller.objects.count()
    return render(request, 'sellerList_admin.html', {'sellers_count': sellers_count})

def user_count_view(request):
    user_count = tbl_user.objects.count()
    return render(request, 'customerList_admin.html', {'user_count': user_count})
    
@login_required(login_url='signin')
def profile_update(request):
    user = request.user  # Assuming the authenticated user

    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        # Handle the case where the profile doesn't exist for the user
        user_profile = None

    if request.method == 'POST':
         first_name = request.POST.get('firstName')
         last_name = request.POST.get('lastName')
         email = request.POST.get('email')
         phone_number = request.POST.get('phoneNumber')
         profile_image = request.FILES.get('profileImage')
          # Update user's basic information
         user.first_name = first_name
         user.last_name = last_name
         user.email = email
         user.save()
                # Update or create user profile
         if user_profile:
            user_profile.phone_number = phone_number
            if profile_image:
                user_profile.profile_image = profile_image
         else:
            user_profile = UserProfile(user=user, phone_number=phone_number, profile_image=profile_image)
         user_profile.save()

         messages.success(request, 'Profile updated successfully')
         return redirect('customer_dashboard')  # Redirect to the user's profile page

    # Pass user and user_profile objects to the template for rendering
    context = {
        'user': user,
        'user_profile': user_profile
    }

    return render(request, 'update_profile.html', context)



  
from django.shortcuts import render, redirect
from .models import Seller  # Import your Seller model

def seller_registeration(request):
    if request.method == 'POST':
        # Access form data directly from request.POST and request.FILES
        full_name = request.POST.get('name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        government_identity = request.POST.get('governmentIdentity')
        pan_number = request.POST.get('panNumber')
        business_name = request.POST.get('businessName')
        business_address = request.POST.get('businessAddress')
        business_email = request.POST.get('businessEmail')
        business_phone = request.POST.get('businessPhone')
        business_registration_number = request.POST.get('businessRegistrationNumber')
        gst_number = request.POST.get('vatNumber')
        certificate_pdf = request.FILES.get('certificatePdf')
        bank_account_number = request.POST.get('bankAccountNumber')
        bank_name = request.POST.get('bankName')
        bank_branch = request.POST.get('bankBranch')
        ifsc_code = request.POST.get('ifscCode')
        # Fetch other form fields similarly

        # Create a Seller instance with form data
        seller = Seller(
            full_name=full_name,
            email=email,
            username=username,
            government_identity=government_identity,
            pan_number=pan_number,
            business_name=business_name,
            business_address=business_address,
            business_email=business_email,
            business_phone=business_phone,
            business_registration_number=business_registration_number,
            gst_number=gst_number,
            certificate_pdf=certificate_pdf,
            bank_account_number=bank_account_number,
            bank_name=bank_name,
            bank_branch=bank_branch,
            ifsc_code=ifsc_code,
            # Assign other fields similarly
        )
        seller.save()
        return redirect('seller_waiting')  # Redirect to the waiting page after successful registration
    
    return render(request, 'seller_registeration.html')


def seller_waiting(request):
    return render(request,'seller_waiting.html')


def seller_dashboard(request):
    return render(request,'seller_dashboard.html')

def shop(request):
    return render(request,'shop.html')

def add_product(request):
    return render(request,'add_prod.html')

def details(request):
    return render(request,'detail.html')

def cart(request):
    return render(request,'cart.html')

def checkout(request):
    return render(request,'checkout.html')

def contact(request):
    return render(request,'contact.html')

def base(request):
    return render(request,'base.html')

def customer_dashboard(request):
    return render(request,'customer_dashboard.html')

def admin_authenticate(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

    
        user = authenticate(username=username, password=password)

        if user is not None and user.is_staff and user.username == 'admin':
            login(request, user)
            return redirect('dashboard')  # Replace 'dashboard' with your admin dashboard URL name

    return redirect('signin')

def change_password(request):
    if request.method == 'POST' and request.user.is_authenticated:
        current_password = request.POST.get('currentPassword')
        new_password = request.POST.get('newPassword')
        confirm_password = request.POST.get('confirmPassword')

        # Check if the new password and confirm password match
        if new_password != confirm_password:
            error_message = "New password and confirm password do not match."
            return render(request, 'change_password.html', {'error_message': error_message})

        # Check if the current password matches the user's password
        if not check_password(current_password, request.user.password):
            error_message = "Current password is incorrect."
            return render(request, 'change_password.html', {'error_message': error_message})

        # Update the user's password
        request.user.set_password(new_password)
        request.user.save()

        # Update the session hash to keep the user logged in
        update_session_auth_hash(request, request.user)

        messages.success(request, 'Password Changed Successfully')
        # Redirect to a success page or a profile page
        return redirect('customer_dashboard')

    return render(request, 'change_password.html')


  