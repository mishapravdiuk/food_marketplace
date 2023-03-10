from django.shortcuts import redirect, render
from .forms import UserForm
from vendor.forms import VendorForm
from .models import User, UserProfile
from .utils import detectUser, send_verification_email
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test

from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.template.defaultfilters import slugify
from orders.models import Order

from vendor.models import Vendor
import datetime



# Create your views here.

# Restrict the vendor from accessing the customer page.
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied

# Restrict the customer from accessing the vendor page.
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied



def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")  
        return redirect('dashboard') 
    # We need to check if the method is POST and all values are valid
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # we take password from filled data form
            password = form.cleaned_data['password']
            # It means that the form is ready to save and is stored in the user variable 
            user = form.save(commit = False)
            # We define the user role before making a commit to db
            user.role = User.CUSTOMER
            # This row store user password in hash format
            user.set_password(password)
            user.save()

            # Send verification email
            mail_subject = 'Please activate your account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)

            messages.success(request, 'Your account has been registered successfully')
            return redirect('registerUser')
        else: 
            pass
    else:
        form = UserForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/registerUser.html', context)


def activate(request, uidb64, token):
    # Activate the user by setting the is_active status to True
    try:    
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account is activated.')
        return redirect('myAccount')
    else:
        messages.error(request, 'Invalid activation token')
        return redirect('myAccount')

# Func for registration Vendors
def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")  
        return redirect('myAccount') 
    elif request.method == 'POST':
        # store the data and create the user
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES )
        if form.is_valid() and v_form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit = False)
            user.role = User.VENDOR
            user.set_password(password)
            user.save()
            vendor = v_form.save(commit = False)
            # We specify the user and user_profile for our vendor form
            vendor.user = user
            vendor_name = v_form.cleaned_data['vendor_name']
            vendor.vendor_slug = slugify(vendor_name)+'-'+str(user.id)
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()

            # Send verification email
            mail_subject = 'Please activate your account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)

            messages.success(request, 'Your account has been registered successfully! Please wait for approval.' )

            return redirect('login')
        else:
            pass
    else:
        form = UserForm()
        v_form = VendorForm()

    context = {
        'form': form,
        'v_form': v_form,
    }

    return render(request, 'accounts/registerVendor.html', context)


def login(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")  
        return redirect('myAccount')      
    elif request.method == 'POST':
        # We get email from request data using html attribute "name"
        email = request.POST['email']
        password = request.POST['password']

        # Check if user with this email and password exists
        user = auth.authenticate(email=email, password=password)

        # If exists, login using built-in function login()
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in")
            return redirect('myAccount')
        else:
            messages.error(request, "Invalid email or password")
            return redirect('login')

    return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    messages.info(request, "You are now logged out")
    return redirect('login')


@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)


# this decorator checks if the user is logged in
@login_required(login_url='login')
# this decorator checks if the user passes specials conditions
@user_passes_test(check_role_customer)
def custDashboard(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    recent_orders =  orders[:5]
    context = {
        'orders': orders,
        'orders_count': orders.count(),
        'recent_orders': recent_orders,
    }
    return render(request, 'accounts/custDashboard.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
# This func is used to render vendor dashboard info
def vendorDashboard(request):   
    vendor = Vendor.objects.get(user=request.user)
    orders = Order.objects.filter(vendors__in=[vendor.id], is_ordered=True).order_by('-created_at')
    recent_orders = orders[:10]

    # this month's revenue
    current_month = datetime.datetime.now().month
    current_month_orders = orders.filter(vendors__in=[vendor.id], created_at__month=current_month)
    current_month_revenue = 0
    for i in current_month_orders:
        current_month_revenue += i.get_total_by_vendor()['grand_total']

    # total revenue
    total_revenue = 0 
    for i in orders:
        total_revenue += i.get_total_by_vendor()['grand_total']

    context = {
        'orders': orders,
        'orders_count': orders.count(),
        'recent_orders': recent_orders,
        'total_revenue': total_revenue,
        'current_month_revenue': current_month_revenue,
    }
    return render(request, 'accounts/vendorDashboard.html', context)


# func for the email address entering page. And sending email using function from utils.py
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        # Checking if the user with this email exists
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # Send reset password email
            mail_subject =  "Reset your password"
            email_template = 'accounts/emails/reset_password_email.html'
            send_verification_email(request, user, mail_subject, email_template)

            messages.success(request, "Your password reset link has been send to your email address!")
            return redirect('login')
        else:
            messages.error(request, "Account does not exist")
            return redirect ('forgot_password')
    return render(request, 'accounts/forgot_password.html')

# Validating the user before resetting the password function
def reset_password_validate(request, uidb64, token):
    # Validate the user by decoding the token and user pk
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        return redirect('reset_password')
    else:
        messages.error(request, "This link has been expired.")
        return redirect('myAccount')


# Setting new password func
def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, "Your password has been reset")
            return redirect('login')
        else:
            messages.error(request, "Passwords do not match")
            return redirect('reset_password')

    return render(request, 'accounts/reset_password.html')


