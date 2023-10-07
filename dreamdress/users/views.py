
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import auth
from django.contrib.auth import login,authenticate,logout
from .models import tbl_user
from django.contrib import messages
from django.contrib.auth.decorators import login_required 

@login_required(login_url='signin')
def home(request):
    return render(request,'home.html') 


def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def registration(request):
    if request.method=='POST':
        username=request.POST['username']
        if tbl_user.objects.filter(username=username).exists():
            messages.success(request,'Username Already Exists')
            return redirect('registration')
        email=request.POST['email']
        if tbl_user.objects.filter(email=email).exists():
            messages.success(request,'Email Already Exists')
            return redirect('registration')
        password=request.POST['password']
        user=tbl_user(username=username,email=email)
        user.set_password(password)
        user.save()
        return redirect('signin')
    else:
        return render(request,'registration.html')

def signin(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return redirect('signin')

    return render(request,'signin.html')

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('signin')

