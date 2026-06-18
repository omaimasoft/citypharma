from django.contrib import admin
from .models import Marque


@admin.register(Marque)
class MarqueAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)