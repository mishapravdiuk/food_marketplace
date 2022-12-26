from django.shortcuts import redirect, render
from .forms import UserForm
from vendor.forms import VendorForm
from .models import User, UserProfile
from django.contrib import messages

# Create your views here.


def registerUser(request):
    # We need to check if the method is POST and all values are valid
    if request.method == 'POST':
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
    if request.method == 'POST':
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

            return redirect('registerVendor')
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