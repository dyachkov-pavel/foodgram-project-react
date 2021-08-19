from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import RegisterView, LoginView


urlpatterns = [
    path(
        'login/',
        LoginView.as_view(template_name='registration/login.html'),
        name='login'
    ),
    path(
        'logout/',
        LogoutView.as_view(template_name='registration/logout.html'),
        name='logout'
    ),
    path(
        'register/',
        RegisterView.as_view(template_name='reg.html'),
        name='register'),
]
