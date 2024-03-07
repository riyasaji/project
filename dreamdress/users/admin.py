from django.contrib import admin
from django.contrib.auth.models import User
from .models import Tbl_user,Tbl_seller,Tbl_stock,Tbl_size,Tbl_category,Tbl_colour,Tbl_product,Tbl_ProductImage,Tbl_cart,Tbl_cartItem,Tbl_tailor
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):

    def get_queryset(self,request):
        return Tbl_user.objects.exclude(is_superuser=True)

# Register your models here.
admin.site.register(Tbl_user,CustomUserAdmin)
admin.site.register(Tbl_seller)
admin.site.register(Tbl_category)
admin.site.register(Tbl_product)
admin.site.register(Tbl_size)
admin.site.register(Tbl_colour)
admin.site.register(Tbl_ProductImage)
admin.site.register(Tbl_stock)
admin.site.register(Tbl_cart)
admin.site.register(Tbl_cartItem)
admin.site.register(Tbl_tailor)