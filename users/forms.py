from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django import forms


User = get_user_model()

URLS = ['create-recipe', 'download_txt',
        'favourite', 'follow', 'purchases', 'admin']


class CreationForm(UserCreationForm):

    first_name = forms.CharField(required=True, label='Имя')
    last_name = forms.CharField(required=True, label='Фамилия')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    def clean_username(self):
        username = self.cleaned_data['username']
        if username in URLS:
            raise ValidationError(f'Выбранное имя пользователя "{username}" '
                                  'находится в списке URL-адресов сайта')
        return username


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')
