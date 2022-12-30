from django.shortcuts import render, get_object_or_404
from .forms import VendorForm
from accounts.forms import UserProfileForm

from django.contrib import messages

from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.models import UserProfile
from .models import Vendor
from accounts.views import check_role_vendor

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
# func for v_profile template, render 2 forms and update 2 models.
def vprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    # Storing the data in the database
    # First check if the method is POST
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        # Check if the forms are valid
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, "You have successfully updated your restaurant profile!")
        else:
            pass
    else:
        # Thanks to this code and instance this form will load the existing data of this form
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)

    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor,
    }
    return render(request, 'vendor/vprofile.html', context)
