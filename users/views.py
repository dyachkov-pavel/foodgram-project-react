from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CreationForm
from django.contrib.auth import authenticate, login


def register(request):
    if request.method == 'POST':
        form = CreationForm(request.POST)
        if form.is_valid():
            form.save()
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = CreationForm()
    return render(request, 'reg.html', {'form': form})
