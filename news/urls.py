from django.urls import path

from news.views import news_list_view

urlpatterns = [
    path('', news_list_view, name='news')
]