from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, UserProfile, Subscription


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('first_login', 'last_login', 'date_joined')}),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)
admin.site.register(Subscription)
