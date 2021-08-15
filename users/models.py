from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomAccountManager(BaseUserManager):

    def create_user(self, email, username, first_name, password, **other_fields):
        if not email:
            raise ValueError('Необходимо ввести email')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username,
                          first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, first_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        return self.create_user(email, username, first_name, password, **other_fields)


class User(AbstractUser):

    email = models.EmailField(('Email'), unique=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = CustomAccountManager()

    class Meta:
        verbose_name_plural = 'Профили пользователей'
        verbose_name = 'Профиль'

    def __str__(self):
        return self.username
