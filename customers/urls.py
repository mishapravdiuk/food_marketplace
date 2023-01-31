from django.urls import path, include 
from . import views
import accounts.views as AccountViews


urlpatterns = [
    path('', AccountViews.custDashboard, name='customer'),
    path('profile/', views.cprofile, name='cprofile'),
    path('my_orders/', views.my_orders, name='customer_my_orders'),
    path('order_details/<int:order_number>', views.order_details, name='order_detail')
]
