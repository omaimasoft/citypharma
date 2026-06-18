import random
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password


class ClientProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="client_profile"
    )
    phone = models.CharField(max_length=30, blank=True)

    class Meta:
        verbose_name = "Profil client"
        verbose_name_plural = "Profils clients"

    def __str__(self):
        return f"Profil de {self.user.username}"


class PasswordResetOTP(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="password_reset_otps"
    )

    phone = models.CharField(max_length=30)
    code_hash = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    attempts = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Code OTP"
        verbose_name_plural = "Codes OTP"

    def __str__(self):
        return f"OTP pour {self.user.username} - {self.phone}"

    @staticmethod
    def generate_code():
        return str(random.randint(100000, 999999))

    @classmethod
    def create_otp(cls, user, phone):
        code = cls.generate_code()

        otp = cls.objects.create(
            user=user,
            phone=phone,
            code_hash=make_password(code),
            expires_at=timezone.now() + timedelta(minutes=10)
        )

        return otp, code

    def is_expired(self):
        return timezone.now() > self.expires_at

    def verify_code(self, code):
        if self.is_used:
            return False, "Ce code a déjà été utilisé."

        if self.is_expired():
            return False, "Ce code a expiré."

        if self.attempts >= 5:
            return False, "Trop de tentatives. Veuillez demander un nouveau code."

        self.attempts += 1
        self.save(update_fields=["attempts"])

        if not check_password(code, self.code_hash):
            return False, "Code incorrect."

        self.is_used = True
        self.save(update_fields=["is_used"])

        return True, "Code validé."