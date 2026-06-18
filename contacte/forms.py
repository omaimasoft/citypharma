from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = Contact
        fields = ['nom_complet', 'telephone', 'message']
        widgets = {
            'nom_complet': forms.TextInput(attrs={
                'placeholder': 'Votre nom complet',
                'class': 'form-control',
                'autocomplete': 'name'
            }),
            'telephone': forms.TextInput(attrs={
                'placeholder': 'Votre numéro de téléphone',
                'class': 'form-control',
                'autocomplete': 'tel'
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Écrivez votre message ici...',
                'rows': 6,
                'class': 'form-control'
            }),
        }

    def clean_nom_complet(self):
        value = self.cleaned_data['nom_complet'].strip()
        if len(value) < 2:
            raise forms.ValidationError("Veuillez entrer un nom valide.")
        return value

    def clean_telephone(self):
        value = self.cleaned_data['telephone'].strip()
        if len(value) < 9:
            raise forms.ValidationError("Veuillez entrer un numéro valide.")
        return value

    def clean_message(self):
        value = self.cleaned_data['message'].strip()
        if len(value) < 10:
            raise forms.ValidationError("Votre message est trop court.")
        return value

    def clean_website(self):
        value = self.cleaned_data.get('website', '')
        if value:
            raise forms.ValidationError("Spam détecté.")
        return value