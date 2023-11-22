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
    path('signin/registration/', views.registration, name='registration'),
    path('registration/signin/', views.signin, name='signin'),
    path('check_email/',views.check_email,name='check_email'),
    path('check_username/',views.check_username,name='check_username'),
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
    path('shop/',views.shop,name='shop'),
    path('seller_registeration/',views.seller_registeration,name='seller_registeration'),
    path('add_product/',views.add_product,name='add_product'),
    path('details/',views.details,name='details'),
    path('cart/',views.cart,name='cart'),
    path('seller_waiting/',views.seller_waiting,name='seller_waiting'),
    path('seller_dashboard/',views.seller_dashboard,name='seller_dashboard'),
    path('checkout/',views.checkout,name='checkout'),
    path('contact/',views.contact,name='contact'),
    path('admin_authenticate/',views.admin_authenticate,name='admin_authenticate'),
    path('base/',views.base,name='base'),
    path('customer_dashboard/',views.customer_dashboard,name='customer_dashboard'),
    path('change_password/',views.change_password,name='change_password'),
    path('customers/', views.customer_list, name='customer_list'),
    path('sellers/', views.seller_list, name='seller_list'),
    
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)