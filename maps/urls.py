from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.maps_view, name='maps'),
]
