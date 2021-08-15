from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CreationForm


class RegisterView(CreateView):
    form_class = CreationForm
    template_name = 'reg.html'
    success_url = reverse_lazy('index')
