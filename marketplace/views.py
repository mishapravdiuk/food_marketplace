from django.shortcuts import render, get_object_or_404, redirect
from vendor.models import Vendor, OpeningHour
from menu.models import Category, FoodItem
from marketplace.context_processors import get_cart_counter, get_cart_subtotal

from django.db.models import Prefetch
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Cart
from django.db.models import Q
from datetime import date, datetime
from orders.forms import OrderForm
from accounts.models import UserProfile

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

    opening_hours = OpeningHour.objects.filter(vendor=vendor).order_by('day', 'from_hour')

    # Check current day's opening hours
    today_date = date.today()
    today = today_date.isoweekday()
    current_opening_hours = OpeningHour.objects.filter(vendor=vendor, day=today)

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None

    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items,
        'opening_hours': opening_hours,
        'current_opening_hours': current_opening_hours,
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
                    return JsonResponse({'status': 'Success', 'message': 'Increase the cart quantity.', 'cart_counter': get_cart_counter(request), 'qty':chkCart.quantity, 'cart_total': get_cart_subtotal(request)})
                except:
                    chkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status': 'Success', 'message': 'Cart created.', 'cart_counter': get_cart_counter(request), 'qty':chkCart.quantity, 'cart_total': get_cart_subtotal(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist.'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid response.'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue.'})

# func for decreasing amount of items in cart
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
                    return JsonResponse({'status': 'Success', 'cart_counter': get_cart_counter(request), 'qty':chkCart.quantity, 'cart_total': get_cart_subtotal(request)})
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'You dont have this item in your cart'})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist.'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid response.'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue.'})

# Func for rendering and getting item (cart)
@login_required(login_url='login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/cart.html', context)

# func for deleting a cart
def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                # Check if the cart item exists
                cart_item = Cart.objects.filter(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status': 'Success', 'message': 'Cart item has been deleted', 'cart_counter': get_cart_counter(request), 'cart_total': get_cart_subtotal(request)})
            except:
                    return JsonResponse({'status': 'Failed', 'message': 'Cart item does not exist.'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid response.'})
    return 

# func for search bar
def search(request):
    address = request.GET['address']
    latitude = request.GET['lat']
    longitude = request.GET['lng']
    radius = request.GET['radius']
    keyword = request.GET['keyword']


    # get vendor id's that has the food item the user is looking for
    # we getting the list of vendors due to the filter below
    fetch_vendors_by_fooditems = FoodItem.objects.filter(food_title__icontains=keyword, is_available=True).values_list('vendor', flat=True)

    vendors = Vendor.objects.filter(Q(id__in=fetch_vendors_by_fooditems) | Q(vendor_name__icontains=keyword, is_approved=True, user__is_active=True))

    vendor_count = vendors.count()

    context = {
        'vendors': vendors,
        'vendor_count': vendor_count,
    }

    return render(request, 'marketplace/listings.html', context)


# Func for checkout 
@login_required(login_url='login')
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('marketplace')

    user_profile = UserProfile.objects.get(user=request.user)
    default_values = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'phone': request.user.phone_number,
        'email': request.user.email,
        'address': user_profile.address,
        'country': user_profile.country,
        'state': user_profile.state,
        'city': user_profile.city,
        'pin_code': user_profile.pin_code,
    }
    form = OrderForm(initial=default_values)
    

    context = {
        'form': form,
        'cart_items': cart_items,
        'cart_count': cart_count,
    }
    return render(request, 'marketplace/checkout.html', context)
