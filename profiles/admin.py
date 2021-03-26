from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from profiles.user import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    def get_fieldsets(self, request, obj=None):
        return (
            (None, {'fields': ('profile', )}),
            *super().get_fieldsets(request, obj),
        )
