from django.contrib import admin
from django.contrib.auth.models import User
from .models import tbl_user

# Register your models here.
admin.site.register(tbl_user)
