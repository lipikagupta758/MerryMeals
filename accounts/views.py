from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserRegisterationForm
from vendor.forms import VendorRegisterationForm
from .models import User, UserProfile
from .utils import detect_user, send_mail
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from vendor.models import Vendor
# Create your views here.
def registerUser(request):
    if request.method== 'POST':
        form= UserRegisterationForm(request.POST)
        if form.is_valid():
            password= form.cleaned_data['password']
            user= form.save(commit=False)
            user.set_password(password)
            user.role= User.CUSTOMER
            user.save()

            # Send verification mail
            mail_subject='Please activate your account'
            email_template= 'accounts/emails/account_verification_email.html'
            send_mail(request,user, mail_subject, email_template)

            messages.success(request, "Your account has been created successfully!")
            return redirect('registerUser')
    elif request.user.is_authenticated:
        return redirect('myAccount')
    else:
        form= UserRegisterationForm()
    return render(request, 'accounts/registerUser.html', {'form': form})

def registerVendor(request):
    if request.method== 'POST':
        form= UserRegisterationForm(request.POST)
        v_form= VendorRegisterationForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            password= form.cleaned_data['password']
            user= form.save(commit=False)
            user.set_password(password)
            user.role= User.VENDOR
            user.save()
            vendor= v_form.save(commit=False)
            vendor.user= user
            vendor.user_profile= UserProfile.objects.get(user= user)
            vendor.save()
            
            # Send verification mail
            mail_subject='Please activate your account'
            email_template= 'accounts/emails/account_verification_email.html'
            send_mail(request,user, mail_subject, email_template)

            messages.success(request, "Your account has been registered successfully! Please wait for the license approval.")
            return redirect('registerVendor')
    elif request.user.is_authenticated:
        return redirect('myAccount')
    else:
        form= UserRegisterationForm()
        v_form= VendorRegisterationForm()
    return render(request, 'accounts/registerVendor.html', {'form': form, 'v_form': v_form})

def activate(request, uidb64, token):
    # Activating the user
    try:
        uid= urlsafe_base64_decode(uidb64).decode()
        user= User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user= None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active= True
        user.save()
        messages.success(request, "Congrations! Your account is activated.")
        return redirect('myAccount')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('myAccount')

def login(request):
    if request.method=='POST':
        email= request.POST['email']
        password= request.POST['password']
        user= auth.authenticate(email=email,password= password)
        if user is not None:
            auth.login(request, user)
            return redirect('myAccount')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')
    elif request.user.is_authenticated:
        return redirect('myAccount')
    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url= 'login')
def myAccount(request):
    user= request.user
    redirect_url= detect_user(user)
    return redirect(redirect_url)

#Restrict vendor from accessing user page
def check_role_vendor(user):
    if user.role==1:
        return True
    else:
        raise PermissionDenied
    
#Restrict user from accessing vendor page
def check_role_customer(user):
    if user.role==2:
        return True
    else:
        raise PermissionDenied

@login_required(login_url= 'login')
@user_passes_test(check_role_customer)
def customerDashboard(request):
    return render(request, 'customerDashboard.html')

@login_required(login_url= 'login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    # vendor= Vendor.objects.get(user= request.user)
    return render(request, 'vendorDashboard.html')

def forgot_password(request):
    if request.method=='POST':
        email= request.POST['email']
        if User.objects.filter(email=email).exists():
            user= User.objects.get(email__exact= email)

            # send reset password mail
            mail_subject='Reset Your Password'
            email_template= 'accounts/emails/reset_password_email.html'
            send_mail(request,user, mail_subject, email_template)
            messages.success(request, 'Password reset link has been sent to your email address')
            return redirect('login')
        else:
            messages.error(request, 'Email does not exist')
            return redirect('forgot_password')
    return render(request, 'accounts/forgot_password.html')

def reset_password_validate(request, uidb64, token):
    # Validate the user by decoding the token and user pk
    try:
        uid= urlsafe_base64_decode(uidb64).decode()
        user= User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user= None
    
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid']= uid
        messages.success(request, 'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request, 'Link has been expired')
        return redirect('myAccount')

def reset_password(request):
    if request.method=='POST':
        password= request.POST['password']
        confirm_password= request.POST['confirm_password']
        if password== confirm_password:
            pk= request.session.get('uid')
            user= User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active= True
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('reset_password')
    return render(request, 'accounts/reset_password.html')