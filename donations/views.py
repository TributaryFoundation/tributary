from django import shortcuts
from django.conf import settings

from . import forms
from . import models


def index(request):
    return shortcuts.render(request, 'donations/index.html', {})


def start(request):
    return shortcuts.render(request, 'donations/start.html', {})


def info(request):
    if request.method == 'POST':
        form = forms.DonationForm(data=request.POST)
        if form.is_valid():
            if form.cleaned_data['tip']:
                tip = 500 # in cents
            else:
                tip = 0
            models.Donation.objects.create_with_stripe_token(
                stripe_token=form.cleaned_data['stripe_card_token'],
                name=form.cleaned_data['name'],
                email_address=form.cleaned_data['email'],
                monthly_amount=form.cleaned_data['amount'],
                tip=tip,
                instructions=form.cleaned_data['instructions'],
            )
            return shortcuts.redirect('received')
    else:
        form = forms.DonationForm()
    context = {
        'form': form,
        'stripe_publishable_key': settings.STRIPE['publishable_key']
    }
    return shortcuts.render(request, 'donations/info.html', context)


def received(request):
    return shortcuts.render(request, 'donations/received.html', {})


def confirmed(request):
    return shortcuts.render(request, 'donations/confirmed.html', {})

