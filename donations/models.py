import uuid
import urllib.parse

from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db import models
import stripe

from .verification import generate_token


class DonationManager(models.Manager):
    def create_with_stripe_token(self, stripe_token, name, email_address,
            monthly_amount, tip, instructions):
        stripe.api_key = settings.STRIPE['secret_key']
        stripe_customer = stripe.Customer.create(
                source=stripe_token, email=email_address, description=name)
        donation = self.get_queryset().create(
            donor_name=name,
            email_address=email_address,
            monthly_amount=monthly_amount,
            tip=tip,
            instructions=instructions,
            stripe_customer_id=stripe_customer.id,
            email_verified=False,
        )
        return donation

    def verify_email(self, email):
        return self.get_queryset().filter(email_address=email).update(email_verified=True)



class Donation(models.Model):
    '''A Donation represents a single submitted instruction to donations
    on behalf of one of our donors.

    '''
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    email_address = models.EmailField(
        help_text="Email address of the donor who made this donation.",
    )

    email_verified = models.BooleanField(
        help_text="Whether the email address has been verified by the donor.",
    )

    # todo: change these into PositiveIntegerFields
    monthly_amount = models.PositiveIntegerField(
        help_text="Amount to donate each month in cents, not including the tip.",
    )

    tip = models.PositiveIntegerField(
        help_text="The amount in cents to be given to Tributary Foundation out of each monthly charge.",
    )

    instructions = models.TextField(
        help_text="The unstructured instructions describing where the donation should be sent.",
    )

    donor_name = models.CharField(
        help_text="When making a donation, do it on behalf of this name.",
        max_length=1000,
    )

    stripe_customer_id = models.CharField(
        help_text="The id of the customer on stripe.",
        max_length=1000,
    )

    objects = DonationManager()

    def send_verification_email(self, host, scheme='https'):
        url = urllib.parse.urlunsplit((
            scheme,
            host,
            reverse('confirmed'),
            urllib.parse.urlencode({'token': generate_token(self.email_address)}),
            ''
        ))

        send_mail(
            'Almost done! Please verify your Tributary email',
            'Please click this link to verify your email: {link}'.format(link=url),
            'hello@tributary.foundation',
            [ self.email_address ],
            fail_silently=False,
        )


    def __str__(self):
        return '%s <%s>' % (self.donor_name, self.email_address)
