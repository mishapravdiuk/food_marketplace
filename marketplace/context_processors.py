from .models import Cart
from menu.models import FoodItem

# Func for counting items in the cart
def get_cart_counter(request):
    cart_count = 0 
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user)
            if cart_items:
                for cart_item in cart_items:
                    cart_count += cart_item.quantity
            else:
                cart_count = 0
        except:
            cart_counter = 0
    return dict(cart_count=cart_count)

# Func for calculating subtotal and total for cart 
def get_cart_subtotal(request):
    subtotal = 0
    tax = 0
    grand_total =0
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            food_item = FoodItem.objects.get(pk=item.fooditem.id)
            subtotal += (food_item.price * item.quantity)

        grand_total = subtotal + tax
    return dict(subtotal=subtotal, tax=tax, grand_total=grand_total)
