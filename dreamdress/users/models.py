from django.db import models
from django.contrib.auth.models import AbstractUser 


class tbl_user(AbstractUser):
    email=models.EmailField(unique=True)
    
    def __str__(self):
        return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(tbl_user , on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    # Add other fields for the user profile

    def __str__(self):
        return self.user.username + "'s Profile"
