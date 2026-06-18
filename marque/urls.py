
from django.urls import path
from . import views

app_name = 'marque'  # مهم جداً لتفعيل الـ namespace

urlpatterns = [
    path('', views.marque_list, name='liste_marques'),  # الاسم هنا هو liste_marques
    path('<int:marque_id>/', views.marque_detail, name='marque_detail'),
]


app_name = 'marque'


