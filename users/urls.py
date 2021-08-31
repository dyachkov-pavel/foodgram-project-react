from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import RegisterView, LoginView
from django.contrib.auth import views as auth_views

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
        name='register'
    ),
    path(
        'reset/<uidb64>/<token>',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_email.html'),
        name='password_reset_confirm'
    ),
]
