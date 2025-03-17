from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.maps_view, name='maps'),
    path('ajax/get_radiation/', views.get_radiation_view, name='get_radiation_view'),
    path('ajax/get_aqi/', views.get_aqi_view, name='get_aqi_view'),
    path('ajax/get_weather/', views.get_weather_view, name='get_weather_view'),]
