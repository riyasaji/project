from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.contrib.auth.hashers import make_password

#tbl_user
class Tbl_user(AbstractUser):
    email = models.EmailField(unique=True)
    
    USER_TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('seller', 'Seller'),
        ('admin', 'Admin'),
        ('tailor', 'Tailor'),
    )

    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='customer',  
    )

    def __str__(self):
        return self.email


# #Customer Update Profile
# class UserProfile(models.Model):
#     user = models.OneToOneField(Tbl_user , on_delete=models.CASCADE, related_name='profile')
#     phone_number = models.CharField(max_length=15, blank=True, null=True)
#     profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
#     first_name = models.CharField(max_length=100, blank=True, null=True)
#     last_name = models.CharField(max_length=100, blank=True, null=True)
#     # Add other fields for the user profile

#     def __str__(self):
#         return self.user.username + "'s Profile"
    

# Seller Registeration
class Tbl_seller(models.Model):
    PENDING = 'pending'
    REJECTED = 'rejected'
    APPROVED = 'approved'

    ADMIN_APPROVAL_CHOICES = [
        (PENDING, 'Pending'),
        (REJECTED, 'Rejected'),
        (APPROVED, 'Approved'),
    ]

    user = models.OneToOneField(Tbl_user, on_delete=models.CASCADE)
    seller_firstname = models.CharField(max_length=100,null=True)
    seller_lastname = models.CharField(max_length=100,null=True)
    seller_pan_number = models.CharField(max_length=15,null=True)
    seller_phone = models.CharField(max_length=15,null=True)
    seller_address = models.CharField(max_length=255,null=True)
    seller_pincode = models.CharField(max_length=10,null=True)
    seller_district = models.CharField(max_length=100,null=True)
    seller_state = models.CharField(max_length=100,null=True)
    seller_brand_name = models.CharField(max_length=255,null=True)
    seller_license_number= models.CharField(max_length=50,default='')
    seller_license_pdf= models.FileField(upload_to='seller_certificates/',null=True) 
    seller_gst_number = models.CharField(max_length=15,null=True)
    seller_bank_name = models.CharField(max_length=100,null=True)
    seller_bank_account_number = models.CharField(max_length=50,null=True)
    seller_ifsc_code = models.CharField(max_length=20,null=True)
    admin_approval = models.CharField(max_length=10, choices=ADMIN_APPROVAL_CHOICES, default=PENDING)
    seller_form_filled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.seller_firstname} {self.seller_lastname}"
    


#model for category
class Tbl_category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=20, null=False)

#model for colour
class Tbl_colour(models.Model):
    colour_id = models.AutoField(primary_key=True)
    colour_name = models.CharField(max_length=20, null=False)

#brand
class Tbl_brand(models.Model):
    brand_id = models.AutoField(primary_key=True)
    brand_name = models.CharField(max_length=100)

    def __str__(self):
        return self.brand_name


#model for product
class Tbl_product(models.Model):
    product_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Tbl_category, on_delete=models.CASCADE)
    seller = models.ForeignKey(Tbl_seller, on_delete=models.CASCADE)
    product_current_price = models.IntegerField(null=False)
    product_about_product = models.CharField(max_length=200, null=False)  
    product_material = models.CharField(max_length=20, null=False)
    brand = models.ForeignKey(Tbl_brand, on_delete=models.CASCADE,null=True)

    

#model for size
class Tbl_size(models.Model):
    size_id = models.AutoField(primary_key=True)
    size_name = models.CharField(max_length=20, null=False)
    


#model for stock
class Tbl_stock(models.Model):
    stock_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Tbl_product, on_delete=models.CASCADE)
    colour = models.ForeignKey(Tbl_colour, on_delete=models.CASCADE)
    size = models.ForeignKey(Tbl_size, on_delete=models.CASCADE)
    stock_quantity = models.IntegerField(null=False)

#model for productImage
class Tbl_ProductImage(models.Model):
    image_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Tbl_product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/') 


#cart
class Tbl_cart(models.Model):
    user = models.OneToOneField(Tbl_user, on_delete=models.CASCADE)
   

    def __str__(self):
        return f"Cart for {self.user.username}"

# cart -item
class Tbl_cartItem(models.Model):
    cart = models.ForeignKey('Tbl_cart', on_delete=models.CASCADE)
    cart_stock = models.ForeignKey(Tbl_stock, on_delete=models.CASCADE)  # Provide a default value)
    cart_quantity = models.PositiveIntegerField(null=True)
    cart_price=models.PositiveIntegerField(default=1)
    
    def __str__(self):
        if self.cart_stock:
            return f"{self.cart_quantity} - Size: {self.cart_stock.size.size_name}, Color: {self.cart_stock.colour.colour_name}"
        else:
            return f"{self.cart_quantity} x Unknown Product"


#payment
class Tbl_payment(models.Model):
    user = models.ForeignKey(Tbl_user, on_delete=models.CASCADE, null=True, blank=True)
    cart = models.ForeignKey(Tbl_cart, on_delete=models.CASCADE, null=True, blank=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50,null=True)  
    transaction_id = models.CharField(max_length=100,null=True)  

    def __str__(self):
        return f"Payment - {self.payment_date}"

#order
class Tbl_order(models.Model):
    user = models.ForeignKey(Tbl_user, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    order_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment = models.ForeignKey(Tbl_payment, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Order for {self.user.username} - {self.order_date}"

#order-item
class Tbl_orderItem(models.Model):
    order = models.ForeignKey(Tbl_order, on_delete=models.CASCADE)
    product = models.ForeignKey('Tbl_product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order Item: Quantity: {self.quantity}"
    

#wishlist
class Tbl_wishlist(models.Model):
    user = models.ForeignKey(Tbl_user, on_delete=models.CASCADE)
    product = models.ForeignKey(Tbl_product, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wishlist Item {self.user.username}"
    

# review
class Review(models.Model):
    product = models.ForeignKey(Tbl_product, on_delete=models.CASCADE)
    user = models.ForeignKey(Tbl_user, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField()  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user.username}'



# Tbl Tailor
class Tbl_tailor(models.Model):
    PENDING = 'pending'
    REJECTED = 'rejected'
    APPROVED = 'approved'

    ADMIN_APPROVAL_CHOICES = [
        (PENDING, 'Pending'),
        (REJECTED, 'Rejected'),
        (APPROVED, 'Approved'),
    ]

    user = models.OneToOneField(Tbl_user, on_delete=models.CASCADE)
    tailor_firstname = models.CharField(max_length=100, null=True)
    tailor_lastname = models.CharField(max_length=100, null=True)
    tailor_pan_number = models.CharField(max_length=15, null=True)
    tailor_phone = models.CharField(max_length=15, null=True)
    tailor_address = models.CharField(max_length=255, null=True)
    tailor_pincode = models.CharField(max_length=10, null=True)
    tailor_district = models.CharField(max_length=100, null=True)
    tailor_state = models.CharField(max_length=100, null=True)
    tailor_brand_name = models.CharField(max_length=255, null=True)
    tailor_license_number = models.CharField(max_length=50, default='')
    tailor_license_pdf = models.FileField(upload_to='tailor_certificates/', null=True)
    tailor_brand_logo = models.ImageField(upload_to='brand_logos/', null=True)
    tailor_gst_number = models.CharField(max_length=15, null=True)
    tailor_bank_name = models.CharField(max_length=100, null=True)
    tailor_bank_branch = models.CharField(max_length=100, null=True)
    tailor_bank_account_number = models.CharField(max_length=50, null=True)
    tailor_ifsc_code = models.CharField(max_length=20, null=True)
    admin_approval = models.CharField(max_length=10, choices=ADMIN_APPROVAL_CHOICES, default=PENDING)
    tailor_form_filled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.tailor_firstname} {self.tailor_lastname}"
    

#demo products for tailoring
class Tbl_tailorDemoProduct(models.Model):
    tailor = models.ForeignKey(Tbl_tailor, on_delete=models.CASCADE, related_name='demo_products')
    product_name = models.CharField(max_length=255)
    product_description = models.TextField()
    product_image = models.ImageField(upload_to='demo_products/')

    def __str__(self):
        return self.product_name



#measurements
from django.contrib.auth import get_user_model

User = get_user_model()

class Tbl_measurements(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='measurements')
    tailor = models.ForeignKey('Tbl_tailor', on_delete=models.CASCADE, related_name='tailor_measurements')
    bust_size = models.FloatField(null=True, blank=True)
    waist_size = models.FloatField(null=True, blank=True)
    hip_size = models.FloatField(null=True, blank=True)
    shoulder_size = models.FloatField(null=True, blank=True)
    inseam = models.FloatField(null=True, blank=True)
    sleeve_length = models.FloatField(null=True, blank=True)
    neck_width = models.FloatField(null=True, blank=True)
    arm_size = models.FloatField(null=True, blank=True)
    upper_body_length = models.FloatField(null=True, blank=True)
    neck_depth = models.FloatField(null=True, blank=True)
    arm_length = models.FloatField(null=True, blank=True)
    armhole_depth= models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Measurements for {self.user.username} by {self.tailor.tailor_firstname} {self.tailor.tailor_lastname}"


User = get_user_model()

class ChatMessage(models.Model):
    tailor = models.ForeignKey('Tbl_tailor', on_delete=models.CASCADE, related_name='chat_messages')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages')
    message_id = models.AutoField(primary_key=True)
    message = models.TextField()
    viewed = models.BooleanField(default=False)
    send_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.message_id} from {self.customer.username} to {self.tailor.tailor_firstname}"
