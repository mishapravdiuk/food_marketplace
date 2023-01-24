from django.shortcuts import render, get_object_or_404
from vendor.models import Vendor
from menu.models import Category, FoodItem
from marketplace.context_processors import get_cart_counter

from django.db.models import Prefetch
from django.http import HttpResponse, JsonResponse
from .models import Cart

# Create your views here.

# Func for main marketplace page
def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count': vendor_count,
    }
    return render(request, 'marketplace/listings.html', context)


# Func for vendor detail page
def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        # Looks for the data by reverse access from foodItem to Category model using related_name. This method is used when we can't get the element from current model but can get from another linked to this.
        Prefetch(
            'fooditems',
            queryset = FoodItem.objects.filter(is_available=True)
        )
    )

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None

    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/vendor_detail.html', context)


# Func for adding items to cart
def add_to_cart(request, food_id):
    # Check if the user is logged in
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # check if the food item exist
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # Check if this item is already in the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # Increase the quantity
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({'status': 'Success', 'message': 'Increase the cart quantity.', 'cart_counter': get_cart_counter(request), 'qty':chkCart.quantity})
                except:
                    chkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status': 'Success', 'message': 'Cart created.', 'cart_counter': get_cart_counter(request), 'qty':chkCart.quantity})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist.'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid response.'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue.'})


def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # check if the food item exist
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # Check if this item is already in the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # Decrease the quantity
                    if chkCart.quantity >= 1:
                        chkCart.quantity -= 1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.quantity = 0
                    return JsonResponse({'status': 'Success', 'cart_counter': get_cart_counter(request), 'qty':chkCart.quantity})
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'You dont have this item in your cart'})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist.'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid response.'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue.'})


