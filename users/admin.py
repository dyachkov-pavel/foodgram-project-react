from django.contrib import admin
from django.db import models
from .models import User
from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea, TextInput


class UserAdminConfig(UserAdmin):
    ordering = ("-date_joined",)
    list_display = ("id", "email", "username", "full_name",
                    "is_active", "is_staff", "is_superuser")
    list_filter = ('is_staff', 'is_superuser', 'is_active',)
    search_fields = ('username', 'full_name', 'email')
    fieldsets = (
        (None, {'fields': ('username', 'full_name', 'email', 'password',)}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser',),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username',
                       'full_name', 'password1',
                       'password2', 'is_staff',
                       'is_superuser', 'is_active',),
        }),
    )


admin.site.register(User, UserAdminConfig)
