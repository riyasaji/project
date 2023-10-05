
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages

def home(request):
    return render(request,'index.html') 

def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def signin(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
    return render(request,'signin.html')

def registration(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        confirmpassword=request.POST['confirmpassword']
        if User.objects.filter(email=email).exits():
            messages.info(request,"Email already exists.")
        else:
            user=User.objects.create_user(username=username,email=email,password=password)
            user.save();
        return redirect('/')
    else:
        return render(request,'registration.html')

