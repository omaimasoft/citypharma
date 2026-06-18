from django.contrib import admin
from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'telephone', 'date_envoi', 'short_message')
    list_filter = ('date_envoi',)
    search_fields = ('nom_complet', 'telephone', 'message')
    ordering = ('-date_envoi',)
    readonly_fields = ('date_envoi',)

    fieldsets = (
        ('Informations client', {
            'fields': ('nom_complet', 'telephone')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Informations système', {
            'fields': ('date_envoi',)
        }),
    )

    def short_message(self, obj):
        if len(obj.message) > 60:
            return obj.message[:60] + "..."
        return obj.message
    short_message.short_description = "Message"

def __str__(self):
    return f"{self.nom_complet} - {self.telephone}"    