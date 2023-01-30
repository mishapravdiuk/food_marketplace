from vendor.models import Vendor
from django.conf import settings
from accounts.models import UserProfile


# We are fetching the vendor using login user 
def get_vendor(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except:
        vendor = None
    return dict(vendor=vendor)


def get_user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except:
        user_profile = None
    return dict(user_profile=user_profile)


# Function to get google_api_key from settings to template
def get_google_api(request):
    return {'GOOGLE_API_KEY': settings.GOOGLE_API_KEY}


def get_paypal_client_id(request):
    return {'PAYPAL_CLIENT_ID': settings.PAYPAL_CLIENT_ID}