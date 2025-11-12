from django.contrib import admin
from django.urls import path,include
from users.views import Register

urlpatterns = [
    path('register/',Register.as_view(), name='register'),
    # path('login/',Login.as_view(),name='login'),
    # path('dashboard/',Home.as_view(), name='Dashboard'),
    path('vendor/register/',Register.as_view(), name='vendor-register')
]