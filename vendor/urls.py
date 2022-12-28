from django.urls import path
from . import views
from accounts import views as AccountsViews


urlpatterns = [
    path('', AccountsViews.vendorDashboard, name='dashboard'),
    path('profile/', views.vprofile, name='vprofile'),
]
