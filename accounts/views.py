from django.shortcuts import redirect, render
from .forms import UserForm
from vendor.forms import VendorForm
from .models import User, UserProfile
from .utils import detectUser
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test

from django.core.exceptions import PermissionDenied


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
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()

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
    return render(request, 'accounts/custDashboard.html')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request, 'accounts/vendorDashboard.html')