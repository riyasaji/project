
from django.shortcuts import render,redirect
from django.contrib.auth.models import auth
from django.contrib.auth import login,authenticate,logout as auth_logout
from .models import Tbl_user,Tbl_seller,Tbl_category,Tbl_colour,Tbl_product,Tbl_ProductImage,Tbl_size,Tbl_stock,Tbl_tailor,Tbl_cart,Tbl_cartItem,Tbl_payment,Tbl_wishlist,Tbl_orderItem,Tbl_order,Tbl_brand,Review,Tbl_tailorDemoProduct,Tbl_measurements
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
from django.http import HttpResponseServerError
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
from django.db.models import Q
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
    cart_item_count = 0
    wishlist_count = 0
    
    if request.user.is_authenticated:
        cart_item_count = Tbl_cartItem.objects.filter(cart__user=request.user).count()
        wishlist_count = Tbl_wishlist.objects.filter(user=request.user).count()
    categories = Tbl_category.objects.all()
    sizes = Tbl_size.objects.all()  # Fetch all categories
    return render(request, 'home.html', {'cart_item_count': cart_item_count, 'wishlist_count': wishlist_count, 'categories': categories,'sizes':sizes})

# categories = Tbl_category.objects.all()
# 'categories': categories

def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

#customer registeration
@never_cache
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
                elif user.user_type == 'tailor':
                    try:
                        tailor = Tbl_tailor.objects.get(user=user)
                        print("tailor: ", tailor)
                        if tailor.admin_approval == 'pending':
                            return redirect('tailor_updateProfile')
                        elif tailor.admin_approval == 'approved':
                            return redirect('tailor_dashboard')
                        else:
                            messages.error(request, 'Your tailor account has been rejected by the admin.')
                            return redirect('signin')
                    except Tbl_tailor.DoesNotExist:
                        messages.error(request, 'Tailor account not found.')
                        return redirect('tailor_updateProfile')
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
         request.session.flush()
         auth_logout(request)
    
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
    


#check email
def check_email(request):
    email= request.GET.get('email','')
    email_exists = Tbl_user.objects.filter(email=email).exists()
    return JsonResponse({'exists': email_exists})


#seller registeration
@never_cache
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
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
@login_required(login_url='signin')
@never_cache
def seller_dashboard(request):
    seller_products = request.user.tbl_seller.tbl_product_set.all()

    product_sales = {}

    # Calculate the number of products sold for each product
    for product in seller_products:
        # Filter order items related to the current product
        order_items = Tbl_orderItem.objects.filter(product=product)
        # Calculate total quantity sold for the current product
        total_quantity_sold = sum(order_item.quantity for order_item in order_items)
        # Store product sales data in dictionary with brand name and category
        product_info = (product.brand.brand_name, product.category.category_name)
        product_sales[product_info] = total_quantity_sold

    return render(request, 'seller_dashboard.html', {'product_sales': product_sales})

#tailor_dashboard
@login_required(login_url='signin')
@never_cache
def tailor_dashboard(request):
    return render(request,'tailor_dashboard.html')

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

from django.template.defaulttags import register

@register.filter
def range_stars(value):
    return range(value)

@register.filter
def inverse_range_stars(value):
    return range(5 - value)

#product -details , detail.html
@never_cache
def details(request, product_id):
    product = get_object_or_404(Tbl_product, pk=product_id)
    product_images = list(Tbl_ProductImage.objects.filter(product=product))
    product_images_with_index = [(index, image) for index, image in enumerate(product_images)]
    sizes = Tbl_size.objects.filter(tbl_stock__product=product).distinct()
    colors = Tbl_colour.objects.filter(tbl_stock__product=product).distinct()
    print("Product Images:", product_images) 
    similar_products = Tbl_product.objects.filter(category=product.category).exclude(pk=product_id)[:3]
    reviews = Review.objects.filter(product=product)
    cart_item_count=0
    wishlist_count=0
    if request.user.is_authenticated:
            cart_item_count = Tbl_cartItem.objects.filter(cart__user=request.user).count()
            wishlist_count = Tbl_wishlist.objects.filter(user=request.user).count()

    return render(request, 'detail.html', {
        'product': product,
       'product_images_with_index': product_images_with_index,
        'sizes': sizes,
        'sizes': sizes,
        'colors': colors,
        'similar_products': similar_products,
        'cart_item_count': cart_item_count, 
        'wishlist_count': wishlist_count,
        'reviews': reviews
    })



@login_required
@never_cache
def add_to_cart(request, product_id):
    product = get_object_or_404(Tbl_product, pk=product_id)
    if request.method == 'POST':
        quantity = request.POST.get('quantity', 1)
        size_name = request.POST.get('size')
        color_name = request.POST.get('color')
        print("Quantity:", quantity)
        print("Size:", size_name)
        print("Color:", color_name)
        if not quantity:
            quantity = 1

        
        stock = get_object_or_404(Tbl_stock, product=product, colour__colour_name=color_name, size__size_name=size_name)
        print("Stock:", stock)

        if int(quantity) > stock.stock_quantity:
            print("Stock finished.")
            return redirect('details')  
    
        cart, created = Tbl_cart.objects.get_or_create(user=request.user)
        
   
        cart_item = Tbl_cartItem.objects.filter(cart=cart, cart_stock=stock).first()
        print("Cart:", cart)
        print("Cart Item:", cart_item)

        if cart_item:
            # If the item already exists, update the quantity
            cart_item.cart_quantity += int(quantity)
            cart_item.save()
        else:
            # If the item does not exist, create a new cart item
            cart_item = Tbl_cartItem.objects.create(cart=cart, cart_stock=stock, cart_quantity=int(quantity))
            
        return redirect('view_cart')  
    else:   
        if request.user.is_authenticated:
            return render(request, 'detail.html', {'product': product})
        else:
            # Redirect to popup_message view if user is not authenticated
            messages.info(request, 'Please sign in or register to add items to your cart.')
            return redirect('popup_message')




# view my cart
@never_cache
def view_cart(request):
    cart_items = Tbl_cartItem.objects.all()  # Fetch cart items from the database
    subtotal = 0  # Initialize subtotal variable
    total=0
    for cart_item in cart_items:
        cart_item.total_price = cart_item.cart_stock.product.product_current_price * cart_item.cart_quantity
        subtotal += cart_item.total_price  # Add each item's total price to subtotal
        total = subtotal + 10 

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'total': total
    }

    if request.user.is_authenticated:
        cart_item_count = Tbl_cartItem.objects.filter(cart__user=request.user).count()
        wishlist_count = Tbl_wishlist.objects.filter(user=request.user).count()
        context.update({
            'cart_item_count': cart_item_count,
            'wishlist_count': wishlist_count
        })

    return render(request, 'cart.html', context)


#cart_count
def cart_item_count(request):
    cart_item_count = 0
    if request.user.is_authenticated:
        cart_item_count = Tbl_cartItem.objects.filter(cart__user=request.user).count()
    return {'cart_item_count': cart_item_count}


#payment
import razorpay

@login_required
def initiate_payment(request):
    total, order_amount = calculate_total_and_order_amount(request.user)
    order_id = create_order(order_amount)
    payment_method = "Online Payment"  
    transaction_id = "1234567890"  # Example: You can customize this based on your requirements
    # Create Tbl_payment instance to store payment details
    payment = Tbl_payment.objects.create(
        user=request.user,
        cart=request.user.tbl_cart,
        payment_amount=order_amount / 100,  
        payment_method=payment_method,
        transaction_id=transaction_id
    )
    return render(request, 'razorpay_checkout.html', {'order_id': order_id, 'order_amount': order_amount})

def calculate_total_and_order_amount(user):
    cart_items = Tbl_cartItem.objects.filter(cart__user=user)
    subtotal = 0
    
    for cart_item in cart_items:
        cart_item.total_price = cart_item.cart_stock.product.product_current_price * cart_item.cart_quantity
        subtotal += cart_item.total_price
    
    total = subtotal + 10
    order_amount = total * 100
    
    return total, order_amount

def create_order(order_amount):
    client = razorpay.Client(auth=('rzp_test_GfzsM6qWehBGju','4ZZkYgLAtHFGy89EjiHpDCyE'))
    order_currency = 'INR'
    order_receipt = 'order_rcptid_11'
    notes = {'Shipping address': 'Dummy Address'}
    order = client.order.create({'amount': order_amount, 'currency': order_currency, 'receipt': order_receipt, 'notes': notes})
    
    return order['id']

from django.db import transaction
from django.db import transaction
from django.db.models import F

def success(request):
    user_cart = Tbl_cart.objects.get(user=request.user)
    cart_items = user_cart.tbl_cartitem_set.all()  

    with transaction.atomic():
        created_orders = []

        # Create an order for each item in the cart
        for cart_item in cart_items:
            order = Tbl_order.objects.create(
                user=request.user,
                order_amount=cart_item.cart_price,
                # payment=cart_item.cart.payment,  # Assign the payment associated with the cart
                # You can add other fields to the order as needed
            )

            # Create an order item for the current cart item
            Tbl_orderItem.objects.create(
                order=order,
                product=cart_item.cart_stock.product,
                quantity=cart_item.cart_quantity,
                price=cart_item.cart_stock.product.product_current_price,
                # You can add other fields to the order item as needed
            )

            created_orders.append(order)

            # Decrease stock quantity
            stock_item = cart_item.cart_stock
            stock_item.stock_quantity -= cart_item.cart_quantity
            stock_item.save()

        # Once orders are created, delete the cart items
        cart_items.delete()

    return render(request, 'success.html')

@never_cache
def order_history(request):
    user = request.user
    orders = Tbl_order.objects.filter(user=user)
    
   
    order_data = []
    for order in orders:
        order_items = Tbl_orderItem.objects.filter(order=order)
        order_item_data = []
        for order_item in order_items:
            product = Tbl_product.objects.get(pk=order_item.product_id)
            product_image = Tbl_ProductImage.objects.filter(product=product).first()
            existing_review = Review.objects.filter(product=product, user=user).first()
            order_item_data.append({
                'product_id': order_item.product_id,
                'category_name': product.category.category_name,
                'brand_name': product.brand.brand_name,
                'price': order_item.price,
                'quantity': order_item.quantity,
                'image_url': product_image.image.url if product_image else None,
                'existing_review': existing_review
            })
        
        # Append the order and its items to the order_data list
        order_data.append((order, order_item_data))
    
    context = {
        'order_data': order_data,
    }
    
    return render(request, 'oredr_history.html', context)



# revieww
@never_cache
def submit_review(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        user = request.user
        text = request.POST.get('text')
        rating = request.POST.get('rating')

        try:
            product =Tbl_product.objects.get(pk=product_id)
            existing_review = Review.objects.filter(product=product, user=user).first()
           
            if existing_review:
                existing_review.text = text
                existing_review.rating = rating
                existing_review.save()
            else:
                Review.objects.create(
                    product=product,
                    user=user,
                    text=text,
                    rating=rating
                )

            return JsonResponse({'success': True, 'message': 'Review submitted successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

def generate_pdf_bill(request):
    # Create a response object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="transaction_bill.pdf"'

    # Create a PDF document
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # Create data for the PDF (example data)
    data = [
        ['Transaction ID', 'Amount', 'Date'],
        ['123456', '$100', '2024-03-18'],
        ['789012', '$150', '2024-03-19'],
        # Add more rows as needed
    ]

    # Create a table from the data
    table = Table(data)

    # Add style to the table
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    table.setStyle(style)

    # Add table to the elements list
    elements.append(table)

    # Build the PDF document
    doc.build(elements)

    return response




 #error message if the user is not logged in cart   
def popup_cart(request):
    message = "Please sign in or register to add items to your cart."
    return render(request, 'popup_cart.html', {'message': message})

#update quantity , cart.html
def update_quantity(request, cart_item_id):
    if request.method == 'POST' :
        cart_item = get_object_or_404(Tbl_cartItem, pk=cart_item_id)
        new_quantity = int(request.POST.get('quantity', 0))
        if new_quantity > 0:
            cart_item.cart_quantity = new_quantity
            cart_item.save()
            return JsonResponse({'success': True, 'new_quantity': new_quantity})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid quantity'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method or not an AJAX request'})

 #remove from cart   
def delete_cartitem(request, cart_id):
    cart_item = get_object_or_404(Tbl_cartItem, id=cart_id)

    if request.method == 'POST':
        cart_item.delete()
        print("deleted cart item")
        return redirect('view_cart')
    
# Colours for product
def get_colors(request, image_id=None):
    try:
        if image_id is None:
            product_image = Tbl_ProductImage.objects.filter(product=request.product).first()
        else:
            product_image = Tbl_ProductImage.objects.get(image_id=image_id)
        
        product = product_image.product
        colors = list(Tbl_colour.objects.filter(tbl_stock__product=product).values_list('colour_name', flat=True).distinct())
        sizes = list(Tbl_size.objects.filter(tbl_stock__product=product).values_list('size_name', flat=True).distinct())

        return JsonResponse({'colors': colors, 'sizes': sizes})
    except Tbl_ProductImage.DoesNotExist:
        return JsonResponse({'error': 'Product image not found'}, status=404)


#users List
def user_list(request):
    users = Tbl_user.objects.all()
    return render(request, 'user_list.html', {'users': users})

#sellers List
def seller_list(request):
    sellers= Tbl_seller.objects.filter(admin_approval='approved')
    return render(request, 'seller_list.html', {'sellers': sellers})

#tailors List 
def tailor_list(request):
    tailors = Tbl_tailor.objects.filter(admin_approval='approved')
    return render(request, 'tailor_list.html', {'tailors': tailors})

#admin approvals for display in dashboard
def admin_approvals(request):
    pending_sellers = Tbl_seller.objects.filter(admin_approval=Tbl_seller.PENDING)
    pending_tailors = Tbl_tailor.objects.filter(admin_approval=Tbl_tailor.PENDING)
    context = {
        'pending_sellers': pending_sellers,
        'pending_tailors': pending_tailors,
    }
    return render(request, 'admin_approvals.html', context)


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
            brand_id = request.POST.get('brand_id')
            category_id = request.POST.get('category_id')
            about_product = request.POST.get('about_product')
            material = request.POST.get('material')
            current_price = request.POST.get('current_price')
            print(request.method)
            print(brand_id)
            # Retrieve category object
            category = get_object_or_404(Tbl_category, pk=category_id)
            
            # Get the logged-in seller
            seller = request.user.tbl_seller

            # Get the brand object
            brand = get_object_or_404(Tbl_brand, pk=brand_id)
        
            
            # Create the product object
            product = Tbl_product.objects.create(
                seller=seller,
                category=category,
                product_about_product=about_product,
                product_material=material,
                product_current_price=current_price,
                brand=brand
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
        'sizes': Tbl_size.objects.all(),
        'brands': Tbl_brand.objects.all() 
    })

#product - view -shop
def shop_view(request):
    products = Tbl_product.objects.all()
    categories = Tbl_category.objects.all()
    sizes = Tbl_size.objects.all()
    cart_item_count = 0
    wishlist_count = 0

    if request.user.is_authenticated:
        cart_item_count = Tbl_cartItem.objects.filter(cart__user=request.user).count()
        wishlist_count = Tbl_wishlist.objects.filter(user=request.user).count()

    context = {
        'products': products,
        'cart_item_count': cart_item_count,
        'wishlist_count': wishlist_count,
        'categories': categories,
        'sizes': sizes
        

    }

    return render(request, 'shop.html', context)

#   Check for colour  in add product
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

# add Tbl_colour in add product
def add_color(request):
    if request.method == 'POST':
        color_name = request.POST.get('color_name')
        # Create a new color object and save it to the database
        new_color = Tbl_colour(colour_name=color_name)
        new_color.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'error': 'Invalid request method'})
    
#check category in add product
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
    
# add category in add product
def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        new_category = Tbl_category(category_name=category_name)
        new_category.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'error': 'Invalid request method'})

from django.http import JsonResponse
from .models import Tbl_brand

# Check brand in add product
from django.http import JsonResponse
from .models import Tbl_brand

# Check brand in add product
def check_brand(request):
    if request.method == 'GET':
        brand_name = request.GET.get('brand_name')
        if Tbl_brand.objects.filter(brand_name=brand_name).exists():
            # If the brand already exists in the database
            return JsonResponse({'exists': True})
        else:
            # If the brand doesn't exist in the database
            return JsonResponse({'exists': False})
    else:
        return JsonResponse({'error': 'Invalid request method'})

# Add brand in add product
def add_brand(request):
    if request.method == 'GET':
        brand_name = request.GET.get('brand_name')
        if Tbl_brand.objects.filter(brand_name=brand_name).exists():
            # If the brand already exists in the database
            return JsonResponse({'success': False, 'message': 'Brand already exists!'})
        else:
            # If the brand doesn't exist in the database, add it
            new_brand = Tbl_brand(brand_name=brand_name)
            new_brand.save()
            return JsonResponse({'success': True, 'message': 'Brand added successfully!'})
    else:
        return JsonResponse({'error': 'Invalid request method'})


#manage stock
def product_display(request):
    seller_products = Tbl_product.objects.filter(seller=request.user.tbl_seller)

    context = {
        'seller_products': seller_products
    }
    return render(request, 'managestock.html', context)


#manage stock - update with product details
def product_detail(request, product_id):
    product = get_object_or_404(Tbl_product, pk=product_id)
    stock_entries = Tbl_stock.objects.filter(product=product)
    
    if request.method == 'POST':
        stock_id = request.POST.get('stock_id')
        quantity = request.POST.get('quantity')
        
        try:
            quantity = int(quantity)
        except ValueError:
            return redirect('product_detail', product_id=product_id)


        stock_entry = get_object_or_404(Tbl_stock, pk=stock_id)
        stock_entry.stock_quantity = quantity
        stock_entry.save()
        return redirect('product_detail', product_id=product_id)
    context = {
        'product': product,
        'stock_entries': stock_entries,
        
    }
    return render(request, 'product_detail.html', context)


#product detail.html
def get_stock_quantity(product, color, size):
    try:
        stock_entry = Tbl_stock.objects.get(product=product, colour=color, size=size)
        return stock_entry.stock_quantity
    except Tbl_stock.DoesNotExist:
        return 0


#product detail , update the stock
def update_stock(request):
    if request.method == 'POST':
        try:
            stock_id = request.POST.get('stock_id')
            quantity = request.POST.get('quantity')
            print("Stock ID:", stock_id)
            print("Quantity:", quantity)
            
            stock_entry = Tbl_stock.objects.get(pk=stock_id)
            print("Stock Entry:", stock_entry)
            
            stock_entry.stock_quantity = quantity
            stock_entry.save()
            print("Stock updated:", stock_entry.stock_quantity)

            messages.success(request, 'Stock updated successfully!')
            
            return redirect('product_detail', product_id=stock_entry.product_id)  
        except Tbl_stock.DoesNotExist:
            return HttpResponseServerError("Stock entry does not exist.")
        except Exception as e:
            return HttpResponseServerError("An error occurred: " + str(e))
    else:
        return redirect('product_display')



def not_seller(request):
    return render(request, 'not_seller.html')


# manage_product by admin
def manage_product_admin(request):
    products = Tbl_product.objects.select_related('seller').prefetch_related('tbl_stock_set', 'tbl_productimage_set').all()
    return render(request, 'manage_product.html', {'products': products})


# send email to seller for less stock quantity
def send_message_to_seller(request):
    # Get data from the request
    data = json.loads(request.body)
    seller_email = data.get('email')
    message = data.get('message')
    print(message)
    # Send the email
    try:
        send_mail(
            'Low Stock Alert',
            message,
            'prxnv2832@gmail.com',  
            [seller_email],
            fail_silently=False,
        )
        return JsonResponse({'status': 'success'}, status=200)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)



# search_products
def search_products(request):
    query = request.GET.get('q')
    products = None
    no_results_message = None
    
    print("Search query:", query)  # Debugging: Print the search query
    
    if query:
        products = Tbl_product.objects.filter(
            Q(category__category_name__icontains=query) |
            Q(tbl_stock__colour__colour_name__icontains=query) |
            Q(tbl_stock__size__size_name__icontains=query) |
            Q(product_about_product__icontains=query) |
            Q(product_material__icontains=query)
        ).distinct()
        
        print("Filtered products:", products)  # Debugging: Print the filtered products
        
        if not products:
            # If no products are found for the search query
            no_results_message = "No products found."
    else:
        # If no search query is provided, show all products
        products = Tbl_product.objects.all()
        
        if not products:
            # If there are no products available
            no_results_message = "No products found."
    
    context = {
        'products': products,
        'query': query,
        'no_results_message': no_results_message
    }
    
    return render(request, 'serach_result.html', context)


#autocomplete search bar menu
def autocomplete_products(request):
    query = request.GET.get('q', '')
    suggestions = []

    # Query database for product names containing the query string
    if query:
        products = Tbl_product.objects.filter(product_about_product__icontains=query)[:10]  # Limit to 10 suggestions
        suggestions = [product.product_about_product for product in products]

    return JsonResponse(suggestions, safe=False)









# wishlist
def add_to_wishlist(request, product_id):
    if request.method == "POST" and request.user.is_authenticated:
        user = request.user
        product = Tbl_product.objects.get(product_id=product_id)
        wishlist_item, created = Tbl_wishlist.objects.get_or_create(user=user, product=product)
        if created:
            # Wishlist item was successfully added
            # You can add a success message here if needed
            pass
        else:
            messages.warning(request, 'This item is already in your wishlist.')
        
        wishlist_products = Tbl_wishlist.objects.filter(user=user)
    else:
        wishlist_products = None

    return render(request, 'wishlist.html', {'wishlist_products': wishlist_products}) 


def remove_from_wishlist(request, product_id):
    if request.method == "POST" and request.user.is_authenticated:
        user = request.user
        product = get_object_or_404(Tbl_wishlist, user=user, product_id=product_id)
        product.delete()
        messages.success(request, 'Item removed from your wishlist successfully.')
    else:
        messages.error(request, 'Failed to remove item from wishlist. Please try again later.')

    return redirect('shop') 

def view_wishlist(request):
    cart_item_count = 0
    wishlist_count = 0
    wishlist_products = None

    if request.user.is_authenticated:
        wishlist_products = Tbl_wishlist.objects.filter(user=request.user)
        cart_item_count = Tbl_cartItem.objects.filter(cart__user=request.user).count()
        wishlist_count = wishlist_products.count()

    context = {
        'cart_item_count': cart_item_count,
        'wishlist_count': wishlist_count,
        'wishlist_products': wishlist_products,
    }

    return render(request, 'wishlist.html', context)


# fileter products
def filter_products(request):
    # Retrieve cart item count and wishlist count
    cart_item_count = 0
    wishlist_count = 0
    if request.user.is_authenticated:
        cart_item_count = Tbl_cartItem.objects.filter(cart__user=request.user).count()
        wishlist_count = Tbl_wishlist.objects.filter(user=request.user).count()

    # Retrieve all categories
    categories = Tbl_category.objects.all()
    sizes = Tbl_size.objects.all()

    # Filter products based on selected category
    selected_categories = request.GET.getlist('category')
    if selected_categories:
        products = Tbl_product.objects.filter(category__category_id__in=selected_categories)

    selected_sizes = request.GET.getlist('size')
    if selected_sizes:
        products = products.filter(tbl_stock__size_id__in=selected_sizes)
            


    # Filter products based on price range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price and max_price:
        products = products.filter(product_current_price__gte=min_price, product_current_price__lte=max_price)

    return render(request, 'filter_page.html', {'cart_item_count': cart_item_count, 'wishlist_count': wishlist_count, 'categories': categories, 'sizes': sizes, 'products': products})



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
            return redirect('tailor_registeration')
        username= email
        password=request.POST['password']
        user_type = 'tailor' 
        
        user=Tbl_user.objects.create(username=username,email=email,password=password,user_type=user_type)
        user.set_password(password)
        
        #authentication
        user.is_active=False
        user.save()
        
        Tbl_tailor.objects.create(user=user)

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


#tailor Update Profile
@login_required(login_url='signin')  
@never_cache
def tailor_updateProfile(request):
    tailor = get_object_or_404(Tbl_tailor, user=request.user)
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        pan_number = request.POST.get('panNumber')
        brand_name = request.POST.get('brandName')
        logo = request.FILES.get('logo')
        address = request.POST.get('businessAddress')
        pincode = request.POST.get('pincode')
        district = request.POST.get('district')
        state = request.POST.get('state')
        phone = request.POST.get('businessPhone')
        license_number = request.POST.get('businessRegistrationNumber')
        gst_number = request.POST.get('vatNumber')
        certificate_pdf = request.FILES.get('certificatePdf')
        bank_name = request.POST.get('bankName')
        bank_account_number = request.POST.get('bankAccountNumber')
        ifsc_code = request.POST.get('ifscCode')
        
        # Update existing tailor instance
        tailor.tailor_firstname = firstname
        tailor.tailor_lastname = lastname
        tailor.tailor_pan_number = pan_number
        tailor.tailor_phone = phone
        tailor.tailor_address = address
        tailor.tailor_pincode = pincode
        tailor.tailor_district = district
        tailor.tailor_state = state
        tailor.tailor_brand_name = brand_name
        tailor.tailor_license_number = license_number
        tailor.tailor_gst_number = gst_number
        tailor.tailor_bank_name = bank_name
        tailor.tailor_bank_account_number = bank_account_number
        tailor.tailor_ifsc_code = ifsc_code
        tailor.tailor_license_pdf = certificate_pdf
        tailor.tailor_form_filled = True

        # Handle file upload
        if logo:
            tailor.tailor_brand_logo = logo
        if certificate_pdf:
            tailor.tailor_license_pdf = certificate_pdf
        
        tailor.save()

        product_names = request.POST.getlist('product_name')
        product_descriptions = request.POST.getlist('product_description')
        product_images = request.FILES.getlist('product_image')
        
        # Iterate over product details and create Tbl_tailorDemoProduct instances
        for i in range(len(product_names)):
            product_name = product_names[i]
            product_description = product_descriptions[i]
            product_image = product_images[i]

            # Create a new Tbl_tailorDemoProduct instance
            demo_product = Tbl_tailorDemoProduct.objects.create(
                tailor=tailor,
                product_name=product_name,
                product_description=product_description,
                product_image=product_image
            )
        return redirect('seller_waiting')  

    return render(request,'tailor_updateProfile.html')

# Approve Tailor
def approve_tailor(request, tailor_id):
    if request.method == 'GET':
        try:
            tailor = Tbl_tailor.objects.get(id=tailor_id)
            # Update the admin_approval status to "Approved"
            tailor.admin_approval = 'approved'
            tailor.save()

            # Retrieve the tailor's email from the associated user
            user = tailor.user
            tailor_email = user.email

            # Send approval email
            subject = 'Your tailor account for DreamDress has been approved.'
            message = render_to_string('approval_email.html', {'tailor': tailor})
            plain_message = strip_tags(message)
            send_mail(subject, plain_message, 'prxnv2832@gmail.com', [tailor_email], html_message=message)
            print(subject)
            return JsonResponse({'success': True})
        except Tbl_tailor.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Tailor not found'}, status=404)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

# Reject Tailor
def reject_tailor(request, tailor_id):
    if request.method == 'GET':
        try:
            tailor = Tbl_tailor.objects.get(id=tailor_id)
            # Update the admin_approval status to "Rejected"
            tailor.admin_approval = 'rejected'
            tailor.save()

            # Retrieve the tailor's email from the associated user
            user = tailor.user
            tailor_email = user.email

            # Send rejection email
            subject = 'Your tailor account for DreamDress has been rejected.'
            message = render_to_string('rejection_email.html', {'tailor': tailor})
            plain_message = strip_tags(message)
            send_mail(subject, plain_message, 'prxnv2832@gmail.com', [tailor_email], html_message=message)
            print(subject)
            return JsonResponse({'success': True})
        except Tbl_tailor.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Tailor not found'}, status=404)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

    
    
# dress-type page
def cloth_type(request):
    return render(request,'dresstype.html')











def checkout(request):
    return render(request,'checkout.html')

def contact(request):
    
    cart_item_count = 0
    wishlist_count = 0



    if request.user.is_authenticated:
        cart_item_count = Tbl_cartItem.objects.filter(cart__user=request.user).count()
        wishlist_count = Tbl_wishlist.objects.filter(user=request.user).count()
    return render(request, 'contact.html', {'cart_item_count': cart_item_count, 'wishlist_count': wishlist_count})
   

def tailor_profiles(request):
    tailors = Tbl_tailor.objects.all()
    
    return render(request, 'tailor_profiles.html', {'tailors': tailors})

def tailor_detail(request, tailor_id):
    tailor = get_object_or_404(Tbl_tailor, id=tailor_id)
    demo_products = Tbl_tailorDemoProduct.objects.filter(tailor=tailor)
    return render(request, 'tailor_detail.html', {'tailor': tailor, 'demo_products': demo_products})



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


   