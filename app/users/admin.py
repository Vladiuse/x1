from django.contrib import admin

from users.models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined']


admin.site.register(CustomUser, CustomUserAdmin)
