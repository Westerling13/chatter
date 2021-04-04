from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.template.defaultfilters import safe
from django.urls import reverse

from profiles.models import Profile
from profiles.user import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    readonly_fields = ('profile_link', )

    def get_fieldsets(self, request, obj=None):
        return (
            (None, {'fields': ('profile_link', )}),
            *super().get_fieldsets(request, obj),
        )

    def profile_link(self, obj):
        profile_url = reverse('admin:profiles_profile_change', args=[obj.profile_id])
        return safe(f'<a href="{profile_url}">{obj.profile}</a>')

    profile_link.short_description = 'Профиль'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('user_link', )

    def user_link(self, obj):
        user_url = reverse('admin:profiles_user_change', args=[obj.user.id])
        return safe(f'<a href="{user_url}">{obj.user}</a>')

    user_link.short_description = 'Пользователь'
