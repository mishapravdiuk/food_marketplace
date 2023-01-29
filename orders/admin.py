from django.contrib import admin
from .models import Order, Payment, OrderedFood

# Register your models here.


admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(OrderedFood)