from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from store.models import CustomerOrder


from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm

from .models import ClientProfile, PasswordResetOTP
from .forms import RegisterForm, ProfileUpdateForm, PasswordResetPhoneForm, OTPVerifyForm
from .utils import send_sms



def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("accounts:profile")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {
        "form": form,
    })


@login_required
def profile_view(request):
    recent_orders = (
        CustomerOrder.objects
        .filter(user=request.user)
        .order_by("-created_at")[:3]
    )

    return render(request, "accounts/profile.html", {
        "recent_orders": recent_orders,
    })


@login_required
def edit_profile_view(request):
    if request.method == "POST":
        form = ProfileUpdateForm(
            request.POST,
            instance=request.user,
            user=request.user
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Vos informations ont été mises à jour.")
            return redirect("accounts:profile")
    else:
        form = ProfileUpdateForm(
            instance=request.user,
            user=request.user
        )

    return render(request, "accounts/edit_profile.html", {
        "form": form,
    })


@login_required
def my_orders_view(request):
    orders = (
        CustomerOrder.objects
        .filter(user=request.user)
        .order_by("-created_at")
    )

    return render(request, "accounts/my_orders.html", {
        "orders": orders,
    })


@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(
        CustomerOrder.objects.prefetch_related("items"),
        id=order_id,
        user=request.user
    )

    return render(request, "accounts/order_detail.html", {
        "order": order,
    })


def logout_view(request):
    logout(request)
    return redirect("accounts:login")



def forgot_password_view(request):
    if request.method == "POST":
        form = PasswordResetPhoneForm(request.POST)

        if form.is_valid():
            phone = form.cleaned_data["phone"].strip()

            profile = (
                ClientProfile.objects
                .select_related("user")
                .filter(phone=phone)
                .first()
            )

            if not profile:
                messages.error(request, "Aucun compte trouvé avec ce numéro de téléphone.")
                return redirect("accounts:forgot_password")

            otp, code = PasswordResetOTP.create_otp(
                user=profile.user,
                phone=phone
            )

            send_sms(
                phone,
                f"Votre code de réinitialisation City Pharma Plus est : {code}"
            )

            request.session["password_reset_otp_id"] = otp.id

            messages.success(request, "Un code de vérification a été envoyé.")
            return redirect("accounts:verify_otp")
    else:
        form = PasswordResetPhoneForm()

    return render(request, "accounts/forgot_password.html", {
        "form": form,
    })


def verify_otp_view(request):
    otp_id = request.session.get("password_reset_otp_id")

    if not otp_id:
        messages.error(request, "Veuillez demander un nouveau code.")
        return redirect("accounts:forgot_password")

    otp = get_object_or_404(PasswordResetOTP, id=otp_id)

    if request.method == "POST":
        form = OTPVerifyForm(request.POST)

        if form.is_valid():
            code = form.cleaned_data["code"]
            is_valid, message = otp.verify_code(code)

            if is_valid:
                request.session["password_reset_user_id"] = otp.user.id
                messages.success(request, "Code validé. Choisissez un nouveau mot de passe.")
                return redirect("accounts:reset_password_confirm")

            messages.error(request, message)
    else:
        form = OTPVerifyForm()

    return render(request, "accounts/verify_otp.html", {
        "form": form,
    })


def reset_password_confirm_view(request):
    user_id = request.session.get("password_reset_user_id")

    if not user_id:
        messages.error(request, "Session expirée. Veuillez recommencer.")
        return redirect("accounts:forgot_password")

    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        form = SetPasswordForm(user, request.POST)

        if form.is_valid():
            form.save()

            request.session.pop("password_reset_otp_id", None)
            request.session.pop("password_reset_user_id", None)

            messages.success(request, "Votre mot de passe a été changé avec succès.")
            return redirect("accounts:login")
    else:
        form = SetPasswordForm(user)

    return render(request, "accounts/reset_password_confirm.html", {
        "form": form,
    })