
from django.shortcuts import render,redirect
from django.contrib.auth.models import auth
from django.contrib.auth import login,authenticate,logout,get_user_model
from .models import Tbl_user,Tbl_seller,Tbl_category,Tbl_colour,Tbl_product,Tbl_ProductImage,Tbl_size,Tbl_stock
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
from django.views.decorators.csrf import csrf_protect

#email
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import send_mail

from django.views.decorators.cache import never_cache
from django.utils.html import strip_tags
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
import requests
import json
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
@never_cache
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
@never_cache
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username)

        if username == 'admin' and password == 'Abc1234#':
            user = Tbl_user.objects.filter(username=username).first()
            if user is not None and user.is_superuser:
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                return redirect('dashboard')
        else:
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
@never_cache
@csrf_protect
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
     

#seller update profile
@login_required(login_url='signin')
@never_cache
def seller_updateProfile(request):
    seller = get_object_or_404(Tbl_seller, user=request.user)
    if request.method == 'POST':
        pincode = request.POST.get('pincode')
        if pincode:
            pincode_details = get_pincode_details(pincode)
            if pincode_details:
                seller.seller_pincode = pincode
                seller.seller_district = pincode_details['district']
                seller.seller_state = pincode_details['state']
        seller.seller_firstname = request.POST.get('firstname')
        seller.seller_lastname = request.POST.get('lastname')
        seller.seller_pan_number = request.POST.get('panNumber')
        seller.seller_brand_name = request.POST.get('brandName')
        seller.seller_address = request.POST.get('businessAddress')
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

        return redirect('seller_waiting')
        
    return render(request, 'seller_updateProfile.html', {'seller': seller})

import requests
import logging

# Set up logging
logger = logging.getLogger(__name__)

def get_pincode_details(pincode):
    url = f"https://api.postalpincode.in/pincode/{pincode}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        
        if data:
            first_entry = data[0]
            if first_entry['Status'] == 'Success':
                post_office_details = first_entry.get('PostOffice', [{}])[0]
                city = post_office_details.get('Block')
                state = post_office_details.get('State')
                district = post_office_details.get('District')
                
                if city and state and district:
                    return {
                        'city': city,
                        'state': state,
                        'district': district
                    }
                else:
                    logger.error("City, state, or district not found in API response.")
            else:
                logger.error("API response status is not 'Success'.")
        else:
            logger.error("No data found in API response.")
            
    except requests.RequestException as e:
        logger.error(f"Failed to fetch data. Error: {e}")
        
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        
    return None

#seller_dashboard
@login_required(login_url='signin')
@never_cache
def seller_dashboard(request):
    return render(request,'seller_dashboard.html')

#admin_dashboard
@login_required(login_url='signin')
@never_cache
def dashboard(request):
    customer_count = Tbl_user.objects.filter(user_type='customer').count()
    seller_count = Tbl_user.objects.filter(user_type='seller').count()
    tailor_count = Tbl_user.objects.filter(user_type='tailor').count()
    
    context = {
        'customer_count': customer_count,
        'seller_count': seller_count,
        'tailor_count': tailor_count,
    }
    users = Tbl_user.objects.all()
    return render(request, 'dashboard.html',context)


def extra(request):
    return render(request,'extra.html')

#users List
def user_list(request):
    users = Tbl_user.objects.all()
    return render(request, 'user_list.html', {'users': users})

#sellers List
def seller_list(request):
    sellers= Tbl_seller.objects.filter(admin_approval='approved')
    return render(request, 'seller_list.html', {'sellers': sellers})

#admin approvals for display in dashboard
def admin_approvals(request):
     sellers = Tbl_seller.objects.filter(admin_approval=Tbl_seller.PENDING)
     return render(request, 'admin_approvals.html', {'sellers': sellers})

# Approve Seller
def approve_seller(request, seller_id):
    if request.method == 'GET':
        try:
            seller = Tbl_seller.objects.get(id=seller_id)
            # Update the admin_approval status to "Approved"
            seller.admin_approval = 'approved'
            seller.save()
            print("Approved:", seller_id)

            # Retrieve the seller's email from the associated user
            user = seller.user
            seller_email = user.email

            # Send approval email
            subject = 'Your seller account for DreamDress has been approved.'
            message = render_to_string('approval_email.html', {'seller': seller})
            plain_message = strip_tags(message)
            send_mail(subject, plain_message, 'prxnv2832@gmail.com', [seller_email], html_message=message)
            print(subject)
            return JsonResponse({'success': True})
        except Tbl_seller.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Seller not found'}, status=404)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

# Reject Seller
def reject_seller(request, seller_id):
    if request.method == 'GET':
        try:
            seller = Tbl_seller.objects.get(id=seller_id)
            # Update the admin_approval status to "Rejected"
            seller.admin_approval = 'rejected'
            seller.save()
            print("Rejected:", seller_id)

            # Retrieve the seller's email from the associated user
            user = seller.user
            seller_email = user.email

            # Send rejection email
            subject = 'Your seller account for DreamDress has been rejected.'
            message = render_to_string('rejection_email.html', {'seller': seller})
            plain_message = strip_tags(message)
            send_mail(subject, plain_message, 'prxnv2832@gmail.com', [seller_email], html_message=message)
            print(subject)
            return JsonResponse({'success': True})
        except Tbl_seller.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Seller not found'}, status=404)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    

def customer_list(request):
    customers = Tbl_user.objects.filter(user_type='customer')  # Fetch customers
    return render(request, 'customerList_admin.html', {'customers': customers})

#user count
def user_count_view(request):
    user_count = Tbl_user.objects.count()
    return render(request, 'customerList_admin.html', {'user_count': user_count})
    


#seller waiting page
def seller_waiting(request):
    return render(request,'seller_waiting.html')

# Add Product
@login_required(login_url='signin')  
def add_product(request):
    if request.method == 'POST':
        try:
            # Extract data from the form
            brand_name = request.POST.get('brand_name')
            category_id = request.POST.get('category_id')
            about_product = request.POST.get('about_product')
            material = request.POST.get('material')
            current_price = request.POST.get('current_price')
            
            # Retrieve category object
            category = get_object_or_404(Tbl_category, pk=category_id)
            
            # Get the logged-in seller
            seller = request.user.tbl_seller
            
            # Create the product object
            product = Tbl_product.objects.create(
                seller=seller,
                category=category,
                product_about_product=about_product,
                product_material=material,
                product_current_price=current_price
            )
            
            # Handle stock entries
            colors = request.POST.getlist('colour_id')
            sizes = request.POST.getlist('size_id')
            quantities = request.POST.getlist('stock_quantity[]')
            
            for color_id, size_id, quantity in zip(colors, sizes, quantities):
                colour = get_object_or_404(Tbl_colour, pk=color_id)
                size = get_object_or_404(Tbl_size, pk=size_id)
                
                stock = Tbl_stock.objects.create(
                    product=product,
                    colour=colour,
                    size=size,
                    stock_quantity=quantity
                )
            
            # Handle product images
            product_images = request.FILES.getlist('product_images[]')
            for image in product_images:
                Tbl_ProductImage.objects.create(product=product, image=image)
            
            messages.success(request, 'Product added successfully!')
            return redirect('seller_dashboard')  
        except Exception as e:
            messages.error(request, f'Error occurred while adding product: {str(e)}')
            return redirect('add_product')

    return render(request, 'add_prod.html', {
        'categories': Tbl_category.objects.all(),
        'colors': Tbl_colour.objects.all(),
        'sizes': Tbl_size.objects.all()
    })

#product - view -shop
def shop_view(request):
    products = Tbl_product.objects.all()
    return render(request, 'shop.html', {'products': products})

#   Check for colour  
def check_color(request):
    if request.method == 'POST':
        color_name = request.POST.get('color_name')
        if Tbl_colour.objects.filter(colour_name=color_name).exists():
            # If the color already exists in the database
            return JsonResponse({'exists': True})
        else:
            # If the color doesn't exist in the database
            return JsonResponse({'exists': False})
    else:
        return JsonResponse({'error': 'Invalid request method'})

# add Tbl_colour
def add_color(request):
    if request.method == 'POST':
        color_name = request.POST.get('color_name')
        # Create a new color object and save it to the database
        new_color = Tbl_colour(colour_name=color_name)
        new_color.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'error': 'Invalid request method'})
    
#check category
def check_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        if Tbl_category.objects.filter(category_name=category_name).exists():
            # If the category already exists in the database
            return JsonResponse({'exists': True})
        else:
            # If the category doesn't exist in the database
            return JsonResponse({'exists': False})
    else:
        return JsonResponse({'error': 'Invalid request method'})
    
# add category
def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        new_category = Tbl_category(category_name=category_name)
        new_category.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'error': 'Invalid request method'})



@login_required(login_url='signin')
def profile_update(request):
    # user = request.user  # Assuming the authenticated user

    # try:
    #     user_profile = UserProfile.objects.get(user=user)
    # except UserProfile.DoesNotExist:
    #     # Handle the case where the profile doesn't exist for the user
    #     user_profile = None

    # if request.method == 'POST':
    #      first_name = request.POST.get('firstName')
    #      last_name = request.POST.get('lastName')
    #      email = request.POST.get('email')
    #      phone_number = request.POST.get('phoneNumber')
    #      profile_image = request.FILES.get('profileImage')
    #       # Update user's basic information
    #      user.first_name = first_name
    #      user.last_name = last_name
    #      user.email = email
    #      user.save()
    #             # Update or create user profile
    #      if user_profile:
    #         user_profile.phone_number = phone_number
    #         if profile_image:
    #             user_profile.profile_image = profile_image
    #      else:
    #         user_profile = UserProfile(user=user, phone_number=phone_number, profile_image=profile_image)
    #      user_profile.save()

    #      messages.success(request, 'Profile updated successfully')
    #      return redirect('customer_dashboard')  # Redirect to the user's profile page

    # # Pass user and user_profile objects to the template for rendering
    # context = {
    #     'user': user,
    #     'user_profile': user_profile
    # }

    return render(request, 'update_profile.html')


#change password for customer
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

# #sellerview2
# def sellviews(request):
#     # Retrieve seller profiles with the role 'SELLER'
#     user_profiles = Seller.objects.filter(user_type='seller')

#     # Pass the data to the template
#     context = {'user_profiles': user_profiles}
#     return render(request, 'sellerList_admin.html', context)
     






# def sellor_approval(request):
#     # Filter sellers with status equals 'Pending'
#     unapproved_sellers = Seller.objects.filter(status='Pending')
    
#     return render(request, 'seller_approval.html', {'unapproved_sellers': unapproved_sellers})




# def seller_approval(request, seller_id):
#     seller = Seller.objects.get(pk=seller_id)

#     # Update seller status to 'Approved'
#     seller.status = Seller.APPROVED
#     seller.save()

#     # Send email notification
#     subject = 'Account Activation'
#     message = 'Your seller account has been activated successfully.'
#     from_email = 'prxnv2832@gmail.com'  # Your email address
#     to_email = seller.user.email
#     send_mail(subject, message, from_email, [to_email])
    

    
#     return redirect('seller_viewforapproval')


#block_seller - to block the seller approvel
# def block_seller(request, seller_id):
#     seller = Seller.objects.get(pk=seller_id)
#     seller.is_approved = False
#     seller.save()
#     subject = 'Your Seller Account Has Been blocked'
#     message = 'Dear {},\n\nYour seller account has been blocked by the admin. You cannot  log in and  banned your account.'
#     from_email = 'prxnv2832@gmail.com'  # Replace with your email address
#     recipient_list = [seller.user.email]
    
#     send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    
#     return redirect('sellor_approval')

def delete_seller(request, seller_id):
    user = Tbl_user.objects.get(pk=seller_id)
    user.delete()
    subject = 'Your Seller Account Has Been deleted'
    message = 'Dear {},\n\nYour seller account has been deleted by the admin. You cannot  log in and  banned your account.'
    from_email = 'prxnv2832@gmail.com'  # Replace with your email address
    recipient_list = [user.email]
    
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    return redirect('sellor_approval')


 #tailor registeration
def tailor_registeration(request):
     if request.method=='POST':
        email=request.POST['email']
        if Tbl_user.objects.filter(email=email).exists():
            messages.success(request,'Email Already Exists')
            return redirect('seller_registration')
        username= email
        password=request.POST['password']
        user_type = 'tailor' 
        
        user=Tbl_user.objects.create(username=username,email=email,password=password,user_type=user_type)
        user.set_password(password)
        
        #authentication
        user.is_active=False
        user.save()
        
        # Tbl_tailor.objects.create(user=user)

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
        return render(request,'tailor_registeration.html')   





# def seller_viewforapproval(request):
#     sellers = Seller.objects.filter(status='Pending')
#     return render(request,'seller_approval.html',{'sellers': sellers})



    
    


def product_details(request):
    return render(request, 'details.html')



# def add_product(request):
#     if request.method == 'POST':
#         # Fetch data from the form
#         brand_name = request.POST.get('brand_name')
#         product_name = request.POST.get('product_name')
#         product_number = request.POST.get('product_number')
#         stock = request.POST.get('stock')
#         about_product = request.POST.get('about_product')
#         current_price = request.POST.get('current_price')
#         category_name = request.POST.get('category_name')  # Assuming the category is submitted as a string
#         seller_id = request.POST.get('seller_id')
#         color = request.POST.get('colors')
#         material = request.POST.get('material')
#         image_1 = request.FILES.get('main_image')  # Assuming it's an image file

#         category_instance, created = category.objects.get_or_create(category_name=category_name)
        
#         # Assuming sizes are submitted as a list
#         selected_sizes = request.POST.getlist('sizes')
#         sizes = []
#         for size_name in selected_sizes:
#             size, created = Size.objects.get_or_create(name=size_name)
#             sizes.append(size)

#         # Create the Product instance
#         product = Product.objects.create(
#             brand_name=brand_name,
#             product_name=product_name,
#             product_number=product_number,
#             stock=stock,
#             about_product=about_product,
#             current_price=current_price,
#             category_id=category_instance,
#             seller_id=seller_id,
#             color=color,
#             material=material,
#             image_1=image_1
#         )
        

#         # Add sizes to the product
#         product.save()
#         product.sizes.set(sizes)
#         # Redirect to a success page or do something else
#         messages.success(request, 'Product added successfully!')
#         return redirect('seller_dashboard')  # Replace '/success/' with your desired URL

#     return render(request, 'add_prod.html')  # Assuming the template name is 'add_product.html'




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
    return render(request, 'demo.html')



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


   