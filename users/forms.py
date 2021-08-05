from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.core.exceptions import ValidationError

User = get_user_model()

URLS = ['create-recipe', 'download_txt', 'favourite', 'follow', 'purchases']

class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["full_name", "username", "email", "password1"]

    def clean_username(self):
        username = self.cleaned_data['username']
        if username in URLS:
            raise ValidationError(f"Выбранное имя пользователя '{username}' находится в списке URL-адресов сайта")
        return username
