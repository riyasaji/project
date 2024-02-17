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
    seller_license_pdf= models.FileField(upload_to='certificates/',null=True) 
    seller_gst_number = models.CharField(max_length=15,null=True)
    seller_bank_name = models.CharField(max_length=100,null=True)
    seller_bank_account_number = models.CharField(max_length=50,null=True)
    seller_ifsc_code = models.CharField(max_length=20,null=True)
    admin_approval = models.CharField(max_length=10, choices=ADMIN_APPROVAL_CHOICES, default=PENDING)

    def __str__(self):
        return f"{self.seller_firstname} {self.seller_lastname}"

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