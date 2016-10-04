from django import shortcuts
from django.conf import settings
from django.http import Http404

from . import forms
from . import models
from .verification import validate_token

import structlog
log = structlog.get_logger('trib')

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
            donation = models.Donation.objects.create_with_stripe_token(
                stripe_token=form.cleaned_data['stripe_card_token'],
                name=form.cleaned_data['name'],
                email_address=form.cleaned_data['email'],
                monthly_amount=form.cleaned_data['amount'],
                tip=tip,
                instructions=form.cleaned_data['instructions'],
            )

            donation.send_verification_email(request.get_host(), request.scheme)
            return shortcuts.redirect('received')
        else:
            log.info('invalid donation received', errors=form.errors)
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
    token = request.GET.get('token', '')
    l = log.bind(token=token)

    email = validate_token(token)
    if email is None:
        l.info('failed email verification')
        # The token was invalid or out of date.
        raise Http404("The provided token isn't valid.")

    l = l.bind(email=email)
    l.info('parsed token successfully')
    n_updated = models.Donation.objects.verify_email(email)
    if n_updated == 0:
        l.info('no email found for verification token')
        raise Http404("The provided token isn't valid.")

    return shortcuts.render(request, 'donations/confirmed.html', {})
