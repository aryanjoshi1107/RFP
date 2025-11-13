from django.contrib import admin
from django.urls import path,include
from category.views import AddCategory,Categories,ToggleStatus

urlpatterns = [
    path('',Categories.as_view(),name='Categories'),
    path('add/',AddCategory.as_view(),name='AddCategories'),
    path('togglestatus/<int:pk>/',ToggleStatus.as_view(), name='ToggleStatus'),
]
