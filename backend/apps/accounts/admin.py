from django.contrib import admin
from django.contrib.auth.admin import UserAdmin  
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets
    list_display = ["email", "first_name", "last_name", "is_staff"]
    ordering = ["email"]


admin.site.register(User, CustomUserAdmin)