from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .models import ClientProfile


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        label="Prénom",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    last_name = forms.CharField(
        label="Nom",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )

    phone = forms.CharField(
        label="Téléphone",
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    username = forms.CharField(
        label="Identifiant",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    password2 = forms.CharField(
        label="Confirmer le mot de passe",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "username",
            "password1",
            "password2",
        ]

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Cet email est déjà utilisé.")

        return email

    def save(self, commit=True):
        user = super().save(commit=commit)

        if commit:
            phone = self.cleaned_data.get("phone", "")
            ClientProfile.objects.update_or_create(
                user=user,
                defaults={"phone": phone}
            )

        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Identifiant ou e-mail",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    def clean(self):
        username_or_email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username_or_email and password:
            username = username_or_email

            if "@" in username_or_email:
                try:
                    user = User.objects.get(email__iexact=username_or_email)
                    username = user.username
                except User.DoesNotExist:
                    pass

            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password
            )

            if self.user_cache is None:
                raise self.get_invalid_login_error()

            self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        label="Prénom",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    last_name = forms.CharField(
        label="Nom",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )

    phone = forms.CharField(
        label="Téléphone",
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if self.user:
            profile, created = ClientProfile.objects.get_or_create(user=self.user)
            self.fields["phone"].initial = profile.phone

    def clean_email(self):
        email = self.cleaned_data.get("email")

        qs = User.objects.filter(email__iexact=email)

        if self.user:
            qs = qs.exclude(pk=self.user.pk)

        if qs.exists():
            raise forms.ValidationError("Cet email est déjà utilisé.")

        return email

    def save(self, commit=True):
        user = super().save(commit=commit)

        if commit and self.user:
            phone = self.cleaned_data.get("phone", "")
            ClientProfile.objects.update_or_create(
                user=self.user,
                defaults={"phone": phone}
            )

        return user
    
    
    
    class PasswordResetPhoneForm(forms.Form):
        phone = forms.CharField(
        label="Téléphone",
        max_length=30,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ex: 0612345678"
        })
    )


class OTPVerifyForm(forms.Form):
    code = forms.CharField(
        label="Code de vérification",
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Code reçu par SMS"
        })
    )
    
    
class PasswordResetPhoneForm(forms.Form):
    phone = forms.CharField(
        label="Téléphone",
        max_length=30,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ex: 0612345678"
        })
    )


class OTPVerifyForm(forms.Form):
    code = forms.CharField(
        label="Code de vérification",
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Code reçu par SMS"
        })
    )    