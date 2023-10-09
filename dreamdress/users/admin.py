from django.contrib import admin
from django.contrib.auth.models import User
from .models import tbl_user
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):

    def get_queryset(self,request):
        return tbl_user.objects.exclude(is_superuser=True)

# Register your models here.
admin.site.register(tbl_user,CustomUserAdmin)
