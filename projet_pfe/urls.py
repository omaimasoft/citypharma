from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("admin/", admin.site.urls),

    path("contact/", include("contacte.urls")),

    path("", RedirectView.as_view(url="/store/", permanent=False)),

    path("store/", include(("store.urls", "store"), namespace="store")),

    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),

    path("accounts/", include("accounts.urls")),

    path("marques/", include(("marque.urls", "marque"), namespace="marque")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)