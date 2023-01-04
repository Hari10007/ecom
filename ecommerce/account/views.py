from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib import messages
from django.core.mail import send_mail
from admin_dashboard.forms import UserForm
from django.contrib.auth.forms import AuthenticationForm
import pyotp

import random

# Create your views here.
def admin_login(request):
    if request.user.is_authenticated: 
         return redirect('admin_dash')
    else:
        if request.method == 'POST':
            email  = request.POST['email']
            password = request.POST['password']
            try:
                User.objects.get(email=email,is_staff = True)
                user = authenticate(email = email, password = password)
                if user is not None:
                    login(request,user)
                    return redirect('admin_dash')
                else:
                    messages.error(request, "Invalid password")
            except:
                messages.error(request,"You are not an admin")

    return render(request,"account/admin_login.html")

def user_login(request):
    if request.user.is_authenticated: 
         return redirect('home')
    else:
        if request.method == 'POST':
            email  = request.POST['email']
            password = request.POST['password']
            try:
                user= User.objects.get(email=email, is_admin = False, is_staff= False, is_superuser =False )
                if user.is_active:
                    user = authenticate(email = email, password = password)
                    if user is not None:
                        login(request,user)
                        return redirect('home')
                    else:
                        messages.error(request, "Invalid password")
                else:
                    messages.error(request, "This account is blocked by admin")
            except:
                messages.error(request, "Invalid email")

    return render(request,"account/user_login.html")

def user_create(request):
    if request.user.is_authenticated: 
         return redirect('home')
    else:
        form = UserForm()
        if request.method == 'POST':
            form = UserForm(request.POST)
            if form.is_valid():
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                username = form.cleaned_data['username']
                phone_number = form.cleaned_data['phone_number']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,phone_number=phone_number,
                                    email=email,
                                    password=password)
                secret = pyotp.random_base32()
                totp = pyotp.TOTP(secret, interval=600)
                otp = totp.now()
                send_mail('OTP Login Code', str(otp) ,'harikrishnansr007@gmail.com',[user.email], fail_silently=False)
                context={
                    'user': user
                }
                red = redirect(f'/otp_verification/{user.id}/{secret}', context)
                red.set_cookie("can_otp_enter",True,max_age=600)
                return red  
        context ={
            'form':form
        }

    return render(request,"account/sign_up.html", context)

def otp_login(request):
    if request.user.is_authenticated: 
         return redirect('home')
    else:
        if request.method=="POST":
            if User.objects.filter(email__iexact=request.POST['email']).exists():
                user = User.objects.get(email__iexact=request.POST['email'])
                secret = pyotp.random_base32()
                totp = pyotp.TOTP(secret, interval=600)
                otp = totp.now()
                print(totp.now())
                try:
                    send_mail('OTP Login Code', str(otp) ,'harikrishnansr007@gmail.com',[user.email], fail_silently=False)
                    context={
                        'user': user
                    }
                    red = redirect(f'/otp_verification/{user.id}/{secret}', context)
                    red.set_cookie("can_otp_enter",True,max_age=600)
                    return red  
                except:
                    messages.error(request,"OTP send failed")
            else:
                messages.error(request, "Invalid email")

    return render(request,"account/otp_login.html")

def otp_verification(request,id,secret):
    if request.user.is_authenticated: 
         return redirect('home')
    else:
        if request.method=="POST":
            totp = pyotp.TOTP(secret, interval=600)
            print(totp.now())
            user=User.objects.get(id=id) 
            code = request.POST['1'] + request.POST['2'] + request.POST['3'] + request.POST['4'] +request.POST['5'] + request.POST['6']
            if request.COOKIES.get('can_otp_enter')!=None:
                if(totp.verify(code)):
                    if (user.is_verified != True):
                        user.is_verified = True
                        user.save()
                    login(request, user)
                    red=redirect("home")
                    red.set_cookie('verified',True)
                    return red
                else:
                    messages.error(request,"wrong otp")
            else:
                messages.error(request,"10 minutes passed")    
    return render(request,"account/otp_verification.html")



def user_logout(request):
    try:
        logout(request)
    except:
        pass
    return redirect('login')

def admin_logout(request):
    try:
        logout(request)
    except:
        pass
    return redirect('admin_login')