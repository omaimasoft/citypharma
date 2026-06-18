from django.db import models



class SiteSettings(models.Model):
    site_name = models.CharField(max_length=150, default="City Pharma plus")
    logo = models.ImageField(upload_to='site/', blank=True, null=True)

    phone = models.CharField(max_length=30, blank=True, null=True)
    whatsapp = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    hero_title = models.CharField(max_length=200, blank=True, null=True)
    hero_subtitle = models.CharField(max_length=255, blank=True, null=True)

    footer_text = models.TextField(blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Paramètres du site"
        verbose_name_plural = "Paramètres du site"

    def __str__(self):
        return self.site_name