from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.contrib import admin

User = get_user_model()

class UserAdminConfig(UserAdmin):
    ordering = ('-date_joined',)
    list_display = ('id', 'email', 'username', 'first_name', 'last_name',
                    'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active',)
    search_fields = ('username', 'first_name', 'last_name', 'email')
    fieldsets = (
        (None, {'fields': ('username', 'first_name', 'last_name', 'email', 'password',)}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser',),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username',
                       'first_name', 'last_name', 
                       'password1', 'password2', 
                       'is_staff', 'is_superuser', 'is_active',),
        }),
    )

admin.site.unregister(User)
admin.site.register(User, UserAdminConfig)
