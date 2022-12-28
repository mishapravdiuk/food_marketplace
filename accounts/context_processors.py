from vendor.models import Vendor

# We are fetching the vendor using login user 
def get_vendor(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except:
        vendor = None
    return dict(vendor=vendor)