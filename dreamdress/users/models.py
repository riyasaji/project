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

#model for product
class Tbl_product(models.Model):
    product_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Tbl_category, on_delete=models.CASCADE)
    seller = models.ForeignKey(Tbl_seller, on_delete=models.CASCADE)
    product_current_price = models.IntegerField(null=False)
    product_about_product = models.CharField(max_length=200, null=False)  
    product_material = models.CharField(max_length=20, null=False)

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
    tailor_gst_number = models.CharField(max_length=15, null=True)
    tailor_bank_name = models.CharField(max_length=100, null=True)
    tailor_bank_account_number = models.CharField(max_length=50, null=True)
    tailor_ifsc_code = models.CharField(max_length=20, null=True)
    tailor_admin_approval = models.CharField(max_length=10, choices=ADMIN_APPROVAL_CHOICES, default=PENDING)
    tailor_form_filled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.tailor_firstname} {self.tailor_lastname}"


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
            return f"{self.cart_quantity} x {self.cart_stock.product.name} - Size: {self.cart_stock.size.size_name}, Color: {self.cart_stock.colour.colour_name}"
        else:
            return f"{self.cart_quantity} x Unknown Product"

    

# #model for category
# class category(models.Model):
#     category_name = models.CharField(max_length=255)
#     category_description = models.CharField(max_length=900)
#     category_picture = models.ImageField(upload_to='category_pictures/', null=True, blank=True)
#     category_verify = models.BooleanField(default=True)


# #model for subcategory
# # class sub_category(models.Model):  
# #         sub_category_name = models.CharField(max_length=255)
# #         sub_category_description = models.CharField(max_length=900)
# #         sub_category_picture = models.ImageField(upload_to='category_pictures/', null=True, blank=True)
# #         sub_category_verify = models.BooleanField(default=True)
# #         category_id = models.ForeignKey(category, on_delete=models.DO_NOTHING, null=True, blank=True)


# #model for size
# class Size(models.Model):
#     name = models.CharField(max_length=50)


# #model for product
# class Product(models.Model):
#     # Product Information Fields
#     brand_name = models.CharField(max_length=255,null=True)
#     product_name = models.CharField(max_length=255)
#     product_number= models.CharField(max_length=100,unique=True,null=True)
#     stock = models.IntegerField()
#     about_product = models.TextField()
#     current_price = models.DecimalField(max_digits=10, decimal_places=2)
#     category_id = models.ForeignKey(category, on_delete=models.DO_NOTHING,null=True, blank=True)
#     # sub_category_id = models.ForeignKey(sub_category, on_delete=models.DO_NOTHING,null=True, blank=True)
#     seller_id = models.ForeignKey(tbl_user, on_delete=models.DO_NOTHING,null=True, blank=True)
#     color = models.CharField(max_length=255)
#     material = models.CharField(max_length=255)
#     product_status = models.BooleanField(default=True)
#     image_1 = models.ImageField(upload_to='product_main_images/', blank=True, null=True)
#     sizes = models.ManyToManyField(Size)



# #model for images
# class product_images(models.Model):  
#     image_data = models.ImageField(upload_to='product_images/', blank=True, null=True)
#     product_id = models.ForeignKey(Product, on_delete=models.DO_NOTHING, null=True, blank=True)



# #model for cart
# class Cart(models.Model):
#     user           =     models.ForeignKey(tbl_user, on_delete=models.CASCADE,null=True,blank=True)


# class Cart_items(models.Model):
#     user           =     models.ForeignKey(tbl_user, on_delete=models.CASCADE,null=True,blank=True)
#     product        =     models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
#     cart        =     models.ForeignKey(Cart,on_delete=models.CASCADE,null=True,blank=True)
#     quantity       =     models.IntegerField(default=1)
#     cart_verify    =     models.BooleanField(default=False)
#     # id_number_info =     models.IntegerField(default=1)


# class MYcart(models.Model):
#     user           =     models.ForeignKey(tbl_user, on_delete=models.CASCADE,null=True,blank=True)
#     product        =     models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)