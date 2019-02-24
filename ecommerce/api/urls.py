from django.contrib import admin
from django.urls import path, include

from api import views

urlpatterns = [
    # write your URL rules here
    path('products/<int:pk>', views.ProductView.as_view()),
    path('products/', views.ProductView.as_view())
]
