# Create your models here.
from django.db import models

class Marque(models.Model):
    nom = models.CharField(max_length=100, unique=True, verbose_name="Nom de la marque")
    image = models.ImageField(upload_to='marques/', blank=True, null=True)
    description = models.TextField(blank=True, verbose_name="Description")

    def __str__(self):
        return self.nom
