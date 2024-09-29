from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'email')
    fieldsets = (
        (None, {
            "fields": (
                "username", "password"
            ),
        }),
        ("개인정보", {
            "fields": (
                "first_name", "last_name", "fullname", "email", "nickname", "birth"
            )
        }),
        ("권한", {
            "fields": (
                "is_active", "is_staff", "is_superuser"
            )
        }),
        ("중요한 일정", {
            "fields": (
                "last_login", "date_joined"
            )
        }),
    )
    