from django.contrib import admin
from .models import ClientProfile, PasswordResetOTP


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone")
    search_fields = ("user__username", "user__email", "phone")


@admin.register(PasswordResetOTP)
class PasswordResetOTPAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "created_at", "expires_at", "is_used", "attempts")
    list_filter = ("is_used", "created_at", "expires_at")
    search_fields = ("user__username", "user__email", "phone")
    readonly_fields = (
        "user",
        "phone",
        "code_hash",
        "created_at",
        "expires_at",
        "is_used",
        "attempts",
    )