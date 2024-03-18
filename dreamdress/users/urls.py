"""dreamdress URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView

urlpatterns = [
    path('home/',views.home,name='home'),
    path('',views.index,name='index'),
    path('about/',views.about),
    path('signin/',views.signin , name='signin'),
    path('registration/',views.registration , name='registration'),
    path('logout/',views.user_logout, name='logout'),
    path('check_email/',views.check_email,name='check_email'),
    # path('check_username/',views.check_username,name='check_username'),
    # path('demo/',views.demo),
    #path('forgot_password/',views.ForgetPassword, name='forgot_password'),
    # path('change_password/<token>/',views.Change_Password, name='change_password'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(),name='activate'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('profile_update/',views.profile_update,name='update_profile'),
    path('shop/',views.shop_view,name='shop'),
    path('seller_registeration/',views.seller_registeration,name='seller_registeration'),
    path('seller_updateProfile/',views.seller_updateProfile,name='seller_updateProfile'),
    path('add_product/',views.add_product,name='add_product'),
    path('view_cart/',views.view_cart,name='view_cart'),
    path('seller_waiting/',views.seller_waiting,name='seller_waiting'),
    path('seller_dashboard/',views.seller_dashboard,name='seller_dashboard'),
    path('checkout/',views.checkout,name='checkout'),
    path('contact/',views.contact,name='contact'),
    path('admin_authenticate/',views.admin_authenticate,name='admin_authenticate'),
    path('demo/',views.demo,name='demo'),
    path('search/', views.search_products, name='search_products'),
    path('autocomplete/', views.autocomplete_products, name='autocomplete_products'),
    path('details/<int:product_id>/', views.details, name='details'),
    path('get_colors/<int:image_id>/', views.get_colors, name='get_colors'),
    path('customer_dashboard/',views.customer_dashboard,name='customer_dashboard'),
    path('change_password/',views.change_password,name='change_password'),
    path('customers/', views.customer_list, name='customer_list'),
    path('sellers/', views.seller_list, name='seller_list'),
    path('approve_seller/<int:seller_id>/', views.approve_seller, name='approve_seller'),
    path('reject_seller/<int:seller_id>/', views.reject_seller, name='reject_seller'),
    path('popup_cart/', views.popup_cart, name='popup_cart'),
     path('update_quantity/<int:cart_item_id>/',views.update_quantity, name='update_quantity'),
    path('user_list/', views.user_list, name='user_list'),
    path('seller_list/', views.seller_list, name='seller_list'),
    path('admin_approvals/', views.admin_approvals, name='admin_approvals'),
    path('check_color/', views.check_color, name='check_color'),
    path('add_color/', views.add_color, name='add_color'),
    path('check_category/', views.check_category, name='check_category'),
    path('add_category/', views.add_category, name='add_category'),
    path('get_pincode_details/<str:pincode>/', views.get_pincode_details, name='get_pincode_details'),
    path('tailor_registeration/',views.tailor_registeration,name='tailor_registeration'),
    # path('manage_stock/', views.manage_stock, name='manage_stock'),
    # path('not_seller/', views.not_seller, name='not_seller'),
    path('products/', views.product_display, name='product_display'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('update_stock/', views.update_stock, name='update_stock'),
    path('manage_product_admin/', views.manage_product_admin,name='manage_product_admin'),
    path('send-message-to-seller/', views.send_message_to_seller, name='send_message_to_seller'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('delete_cartitem/<int:cart_id>/', views.delete_cartitem, name='delete_cartitem'),
    path('add-to-wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('view_wishlist/',views.view_wishlist,name='view_wishlist'),
    path('filter_products/',views.filter_products,name='filter_products'),
    path('success/', views.success, name='success'),
    path('initiate-payment/', views.initiate_payment, name='initiate_payment'),
    path('generate-pdf-bill/', views.generate_pdf_bill, name='generate_pdf_bill'),
    

]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)