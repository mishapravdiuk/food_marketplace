from vendor.models import Vendor
from django.conf import settings

# We are fetching the vendor using login user 
def get_vendor(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except:
        vendor = None
    return dict(vendor=vendor)


# Function to get google_api_key from settings to template
def get_google_api(request):
    return {'GOOGLE_API_KEY': settings.GOOGLE_API_KEY}