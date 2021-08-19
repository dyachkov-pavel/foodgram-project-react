from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CreationForm, LoginForm
from django.contrib.auth import views as auth_views


class RegisterView(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('index')


class LoginView(auth_views.LoginView):
    form_class = LoginForm
