from django.contrib import admin
from django.urls import path,include
from users.views import Register,MyLoginView,Dashboard

urlpatterns = [
    path('register/',Register.as_view(), name='register'),
    path('dashboard/',Dashboard.as_view(), name='Dashboard'),
    path('vendor/register/',Register.as_view(), name='vendor-register')
]