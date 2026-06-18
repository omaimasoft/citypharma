from django import forms
from .models import AvisClient

class AvisClientForm(forms.ModelForm):
    class Meta:
        model = AvisClient
        fields = ['note', 'commentaire']
        widgets = {
            'note': forms.Select(attrs={'class': 'form-control'}),
            'commentaire': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
