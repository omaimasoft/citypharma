from django.db import models
from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r'^\+?[0-9\s\-]{9,20}$',
    message="Entrez un numéro de téléphone valide."
)

class Contact(models.Model):
    nom_complet = models.CharField(max_length=150)
    telephone = models.CharField(max_length=20, validators=[phone_validator])
    message = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.nom_complet} - {self.telephone}"