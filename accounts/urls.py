from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    register_view,
    profile_view,
    edit_profile_view,
    my_orders_view,
    order_detail_view,
    forgot_password_view,
    verify_otp_view,
    reset_password_confirm_view,
    logout_view,
)

from .forms import LoginForm

app_name = "accounts"

urlpatterns = [
    # Connexion
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="accounts/login.html",
            authentication_form=LoginForm
        ),
        name="login"
    ),

    # Inscription
    path("register/", register_view, name="register"),

    # Mon compte
    path("profile/", profile_view, name="profile"),
    path("modifier-mon-compte/", edit_profile_view, name="edit_profile"),

    # Changer mot de passe داخل الحساب
    path(
        "changer-mot-de-passe/",
        auth_views.PasswordChangeView.as_view(
            template_name="accounts/change_password.html",
            success_url="/accounts/profile/"
        ),
        name="change_password"
    ),

    # Mot de passe oublié par SMS OTP
    path(
        "mot-de-passe-oublie/",
        forgot_password_view,
        name="forgot_password"
    ),
    path(
        "verifier-code/",
        verify_otp_view,
        name="verify_otp"
    ),
    path(
        "nouveau-mot-de-passe/",
        reset_password_confirm_view,
        name="reset_password_confirm"
    ),

    # Commandes
    path("mes-commandes/", my_orders_view, name="my_orders"),
    path("mes-commandes/<int:order_id>/", order_detail_view, name="order_detail"),

    # Déconnexion
    path("logout/", logout_view, name="logout"),
]