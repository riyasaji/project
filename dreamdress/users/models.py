from django.db import models
from django.contrib.auth.models import AbstractUser 
 

#user Table
class tbl_user(AbstractUser):
    email = models.EmailField(unique=True)
    
    USER_TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('seller', 'Seller'),
    )

    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='customer',  # You can set a default value if needed
    )

    def __str__(self):
        return self.email


#Customer Update Profile
class UserProfile(models.Model):
    user = models.OneToOneField(tbl_user , on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    # Add other fields for the user profile

    def __str__(self):
        return self.user.username + "'s Profile"
    

# seller Registeration
class Seller(models.Model):
    from users.models import tbl_user
    user = models.OneToOneField(tbl_user, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone_number= models.CharField(max_length=10)
    government_identity = models.CharField(max_length=100)
    pan_number = models.CharField(max_length=20)
    business_name = models.CharField(max_length=100)
    business_address = models.CharField(max_length=255)
    business_email = models.EmailField()
    business_phone = models.CharField(max_length=15)
    business_registration_number = models.CharField(max_length=50)
    gst_number = models.CharField(max_length=20)
    certificate_pdf = models.FileField(upload_to='certificates/')  # Example: Upload certificate PDF to 'certificates/' directory
    bank_account_number = models.CharField(max_length=30)
    bank_name = models.CharField(max_length=100)
    bank_branch = models.CharField(max_length=100)
    ifsc_code = models.CharField(max_length=20)
    # Add other fields related to the seller profile

    # Choices for status
    PENDING = 'Pending'
    APPROVED = 'Approved'
    REJECTED = 'Rejected'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    
    def __str__(self):
        return f"Seller: {self.user.email}"

