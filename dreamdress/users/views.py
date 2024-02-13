
from django.shortcuts import render,redirect
from django.contrib.auth.models import auth
from django.contrib.auth import login,authenticate,logout,get_user_model
from .models import Tbl_user,Tbl_seller
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponse,JsonResponse
from django.utils.encoding import DjangoUnicodeDecodeError
import re
from django.views.generic import View
from .utils import TokenGenerator,generate_token
from django.core.exceptions import ObjectDoesNotExist
#for activating user account
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash


#email
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import send_mail

from django.views.decorators.cache import never_cache
from django.utils.html import strip_tags
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.tokens import default_token_generator

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

#customer registeration
def registration(request):
    if request.method=='POST':
        email=request.POST['email']
        if Tbl_user.objects.filter(email=email).exists():
            messages.success(request,'Email Already Exists')
            return redirect('registration')
        username= email
        password=request.POST['password']
        user_type = 'customer' 
        user=Tbl_user.objects.create(username=username,email=email,password=password,user_type=user_type)
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
        print(message)
        email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email],)
        EmailThread(email_message).start()
        messages.info(request,"Active your account by clicking the link send to your email")
        return redirect('signin')
    else:
        return render(request,'registration.html')

#login
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        user = authenticate(request,username=username, password=password)
        print(user)
        if user is not None:
             if user.is_active: 
                login(request,user)
                request.session['user_id'] = user.id
                request.session['user_email'] = user.email
                request.session['user_type'] = user.user_type
                if user.user_type == 'seller':
                    try:
                        seller = Tbl_seller.objects.get(user=user)
                        print("seller: ",seller)
                        if seller.admin_approval == 'pending':
                            return redirect('seller_updateProfile')
                        elif seller.admin_approval == 'approved':
                            return redirect('seller_dashboard')
                        else:
                            messages.error(request, 'Your seller account has been rejected by the admin.')
                            return redirect('signin')
                    except Tbl_seller.DoesNotExist:
                        messages.error(request, 'Seller account not found.')
                        return redirect('seller_updateProfile')
                else:
                    return redirect('home')
             else:
                messages.error(request, 'Your account is not yet activated. Please check your email for the activation link.')
                return redirect('signin')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
            return redirect('signin')  
    return render(request, 'signin.html')
                
#logout
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('signin')

#email activation
class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_str(urlsafe_base64_decode(uidb64))
            user=Tbl_user.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.info(request,"Account activated sucessfully")
            return redirect('signin')
        return render(request,"auth/activatefail.html")
    

# def check_username(request):
#     username = request.GET.get('username','')
#     print(username)
#     user_exists = Tbl_user.objects.filter(username=username).exists()
#     return JsonResponse({'exists': user_exists})

#check email
def check_email(request):
    email= request.GET.get('email','')
    email_exists = Tbl_user.objects.filter(email=email).exists()
    return JsonResponse({'exists': email_exists})


#seller registeration
def seller_registeration(request):
     if request.method=='POST':
        email=request.POST['email']
        if Tbl_user.objects.filter(email=email).exists():
            messages.success(request,'Email Already Exists')
            return redirect('seller_registration')
        username= email
        password=request.POST['password']
        user_type = 'seller' 
        
        user=Tbl_user.objects.create(username=username,email=email,password=password,user_type=user_type)
        user.set_password(password)
        
        #authentication
        user.is_active=False
        user.save()
        
        Tbl_seller.objects.create(user=user)

        current_site=get_current_site(request)  
        email_subject="Activate your account"
        message=render_to_string('activate.html',{
                   'user':user,
                   'domain':current_site.domain,
                   'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                   'token':generate_token.make_token(user)


            })
        print(message)

        email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email],)
        EmailThread(email_message).start()
        messages.info(request,"Active your account by clicking the link send to your email")
        return redirect('signin')
     else:
        return render(request,'seller_registeration.html')
     

from django.shortcuts import get_object_or_404

def seller_updateProfile(request):
    seller = get_object_or_404(Tbl_seller, user=request.user)

    if request.method == 'POST':
        seller.seller_firstname = request.POST.get('firstname')
        seller.seller_lastname = request.POST.get('lastname')
        seller.seller_pan_number = request.POST.get('panNumber')
        seller.seller_brand_name = request.POST.get('brandName')
        seller.seller_address = request.POST.get('businessAddress')
        seller.seller_pincode = request.POST.get('pincode')
        seller.seller_district = request.POST.get('district')
        seller.seller_state = request.POST.get('state')
        seller.seller_phone = request.POST.get('businessPhone')
        seller.seller_license_number = request.POST.get('businessRegistrationNumber')
        seller.seller_gst_number = request.POST.get('vatNumber')
        seller.seller_bank_account_number = request.POST.get('bankAccountNumber')
        seller.seller_bank_name = request.POST.get('bankName')
        seller.seller_ifsc_code = request.POST.get('ifscCode')

        # Handle file upload
        if 'certificatePdf' in request.FILES:
            seller.seller_license_pdf = request.FILES['certificatePdf']

        seller.save()

        return redirect('seller_dashboard')
        
    return render(request, 'seller_updateProfile.html', {'seller': seller})

#seller_dashboard
def seller_dashboard(request):
    return render(request,'seller_dashboard.html')

#admin_dashboard
def dashboard(request):
    # recent_users = Tbl_user.objects.all().filter(is_superuser=False).order_by('-last_login')[:10]
    # seller=Tbl_seller.objects.all()
    # sellers_count = seller.count()
    # users = Tbl_user.objects.all()
    # user_count=users.count()
    # pending_sellers = Tbl_seller.objects.filter(status='pending')
    # app=pending_sellers.count()
    # context={
    #     'recent_users': recent_users,
    #     'seller':seller,
    #     'sellers_count': sellers_count,
    #     'users':users,
    #     'user_count':user_count,
    #     'pending_sellers' :pending_sellers,
    #     'app':app,
    # }
    return render(request,'dashboard.html')


def extra(request):
    return render(request,'extra.html')

def customer_list(request):
    customers = Tbl_user.objects.filter(user_type='customer')  # Fetch customers
    return render(request, 'customerList_admin.html', {'customers': customers})
#user count

def user_count_view(request):
    user_count = Tbl_user.objects.count()
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



        

       


     
#seller view
def seller_list(request):
    sellers = Tbl_user.objects.filter(user_type='seller')  # Fetch sellers
    return render(request, 'sellerList_admin.html', {'sellers': sellers})

def seller_count_view(request):
    user=Seller.objects.all()
    sellers_count = user.count()
    return render(request, 'sellerList_admin.html', {'sellers_count': sellers_count})

def activate_user(request, user_id):
    user = Tbl_user.objects.get(id=user_id)
    user.is_active = True
    user.save()
    subject = 'Account Activation'
    html_message = render_to_string('activation_mail.html', {'user': user})
    plain_message = strip_tags(html_message)
    from_email = 'hsree524@gmail.com'
    recipient_list = [user.email]
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
    return redirect('seller_approval')

def deactivate_user(request, user_id):
    user = Tbl_user.objects.get(id=user_id)
    if user.is_superuser:
        return HttpResponse("You cannot deactivat the admin.")
    user.is_active = False
    user.save()
    subject = 'Account Deactivation'
    html_message = render_to_string('deactivation_mail.html', {'user': user})
    plain_message = strip_tags(html_message)
    from_email = 'hsree524@gmail.com'
    recipient_list = [user.email]
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
    # Send an email to the user here
    return redirect('seller_approval')

#sellerview2
def sellviews(request):
    # Retrieve seller profiles with the role 'SELLER'
    user_profiles = Seller.objects.filter(user_type='seller')

    # Pass the data to the template
    context = {'user_profiles': user_profiles}
    return render(request, 'sellerList_admin.html', context)
     






# def sellor_approval(request):
#     # Filter sellers with status equals 'Pending'
#     unapproved_sellers = Seller.objects.filter(status='Pending')
    
#     return render(request, 'seller_approval.html', {'unapproved_sellers': unapproved_sellers})




def seller_approval(request, seller_id):
    seller = Seller.objects.get(pk=seller_id)

    # Update seller status to 'Approved'
    seller.status = Seller.APPROVED
    seller.save()

    # Send email notification
    subject = 'Account Activation'
    message = 'Your seller account has been activated successfully.'
    from_email = 'prxnv2832@gmail.com'  # Your email address
    to_email = seller.user.email
    send_mail(subject, message, from_email, [to_email])
    

    
    return redirect('seller_viewforapproval')


#block_seller - to block the seller approvel
def block_seller(request, seller_id):
    seller = Seller.objects.get(pk=seller_id)
    seller.is_approved = False
    seller.save()
    subject = 'Your Seller Account Has Been blocked'
    message = 'Dear {},\n\nYour seller account has been blocked by the admin. You cannot  log in and  banned your account.'
    from_email = 'prxnv2832@gmail.com'  # Replace with your email address
    recipient_list = [seller.user.email]
    
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    
    return redirect('sellor_approval')

def delete_seller(request, seller_id):
   
    user = Tbl_user.objects.get(pk=seller_id)
    user.delete()
    subject = 'Your Seller Account Has Been deleted'
    message = 'Dear {},\n\nYour seller account has been deleted by the admin. You cannot  log in and  banned your account.'
    from_email = 'prxnv2832@gmail.com'  # Replace with your email address
    recipient_list = [user.email]
    
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    return redirect('sellor_approval')


       



def seller_waiting(request):
    return render(request,'seller_waiting.html')

def seller_viewforapproval(request):
    sellers = Seller.objects.filter(status='Pending')
    return render(request,'seller_approval.html',{'sellers': sellers})

def shop(request):
    products = Product.objects.all()  # Change this query based on your filtering logic

    return render(request, 'shop.html', {'products': products})
    

def product_details(request,product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'product': product,
    }
    return render(request,'detail.html', context)


def add_product(request):
    if request.method == 'POST':
        # Fetch data from the form
        brand_name = request.POST.get('brand_name')
        product_name = request.POST.get('product_name')
        product_number = request.POST.get('product_number')
        stock = request.POST.get('stock')
        about_product = request.POST.get('about_product')
        current_price = request.POST.get('current_price')
        category_name = request.POST.get('category_name')  # Assuming the category is submitted as a string
        seller_id = request.POST.get('seller_id')
        color = request.POST.get('colors')
        material = request.POST.get('material')
        image_1 = request.FILES.get('main_image')  # Assuming it's an image file

        category_instance, created = category.objects.get_or_create(category_name=category_name)
        
        # Assuming sizes are submitted as a list
        selected_sizes = request.POST.getlist('sizes')
        sizes = []
        for size_name in selected_sizes:
            size, created = Size.objects.get_or_create(name=size_name)
            sizes.append(size)

        # Create the Product instance
        product = Product.objects.create(
            brand_name=brand_name,
            product_name=product_name,
            product_number=product_number,
            stock=stock,
            about_product=about_product,
            current_price=current_price,
            category_id=category_instance,
            seller_id=seller_id,
            color=color,
            material=material,
            image_1=image_1
        )
        

        # Add sizes to the product
        product.save()
        product.sizes.set(sizes)
        # Redirect to a success page or do something else
        messages.success(request, 'Product added successfully!')
        return redirect('seller_dashboard')  # Replace '/success/' with your desired URL

    return render(request, 'add_prod.html')  # Assuming the template name is 'add_product.html'




def cart(request):
    return render(request,'cart.html')

def checkout(request):
    return render(request,'checkout.html')

def contact(request):
    return render(request,'contact.html')

def base(request):
    return render(request,'base.html')


def temp(request):
     products = [
        {'id': 1, 'name': 'Product 1', 'description': 'Description for Product 1', 'price': 10.0, 'image': 'product1.jpg'},
        {'id': 2, 'name': 'Product 2', 'description': 'Description for Product 2', 'price': 15.0, 'image': 'product2.jpg'},
        # Add more products here...
    ]
     return render(request,'temp.html',{'products': products})



def demo(request):
    # Fetch all sellers
    sellers = Seller.objects.all()
    
    return render(request, 'demo.html', {'sellers': sellers})



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


 #seller_updateProfile
# def seller_updateProfile(request):
#     if request.method == 'POST':
#         seller_firstname = request.POST.get('firstname')
#         seller_lastname=request.POST.get('lastname')
#         pan_number = request.POST.get('panNumber')
#         brand_name = request.POST.get('brandName')
#         business_address = request.POST.get('businessAddress')
#         business_pincode= request.POST.get('pincode')
#         business_district= request.POST.get('district')
#         business_state= request.POST.get('state')
#         business_phone = request.POST.get('businessPhone')
#         business_license_number = request.POST.get('businessRegistrationNumber')
#         gst_number = request.POST.get('vatNumber')
#         certificate_pdf = request.FILES.get('certificatePdf')
#         bank_account_number = request.POST.get('bankAccountNumber')
#         bank_name = request.POST.get('bankName')
#         ifsc_code = request.POST.get('ifscCode')

#         # Handle file upload
#         if 'certificatePdf' in request.FILES:
#             certificate_pdf = request.FILES['certificatePdf']
#         else:
#             certificate_pdf = None

#         user = request.user

#         seller = Tbl_seller(
#             user=user,
#             seller_firstname=seller_firstname,
#             seller_lastname=seller_lastname,
#             seller_pan_number=pan_number,
#             seller_brand_name=brand_name,
#             seller_address=business_address,
#             seller_pincode=business_pincode,
#             seller_district=business_district,
#             seller_state=business_state,
#             seller_phone=business_phone,
#             seller_license_number=business_license_number,
#             seller_gst_number=gst_number,
#             seller_bank_account_number=bank_account_number,
#             seller_bank_name=bank_name,
#             seller_ifsc_code=ifsc_code,
#             seller_license_pdf=certificate_pdf,
#         )
#         seller.save()

#         return redirect('seller_dashboard')
        
#     return render(request, 'seller_updateProfile.html',{'user': request.user})    