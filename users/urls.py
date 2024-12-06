from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from users.views import  profile_user_view, sign_up_view

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html', success_url='/'), name='login'),
    path('signup/', sign_up_view, name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', profile_user_view, name='profile'),
]
