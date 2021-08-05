from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path


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
    path("register/", views.register, name="register"),
]
