from django.urls import path, include 
from . import views
import accounts.views as AccountViews
from .views import cprofile


urlpatterns = [
    path('', AccountViews.custDashboard, name='customer'),
    path('profile/', views.cprofile, name='cprofile'),
]
