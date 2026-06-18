from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .forms import ContactForm

@require_http_methods(["GET", "POST"])
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Votre message a été envoyé avec succès.")
            return redirect('contact')

        messages.error(request, "Veuillez vérifier les informations du formulaire.")
    else:
        form = ContactForm()

    return render(request, 'contacte/contact.html', {'form': form})