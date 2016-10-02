import uuid

from django.conf import settings
from django.db import models
import stripe

class DonationManager(models.Manager):
    def create_with_stripe_token(self, stripe_token, name, email_address,
            monthly_amount, tip, instructions):
        stripe.api_key = settings.STRIPE['secret_key']
        stripe_customer = stripe.Customer.create(
                source=stripe_token, email=email_address, description=name)
        self.get_queryset().create(
            donor_name=name,
            email_address=email_address,
            monthly_amount=monthly_amount,
            tip=tip,
            instructions=instructions,
            stripe_customer_id=stripe_customer.id,
        )



class Donation(models.Model):
    '''A Donation represents a single submitted instruction to donations
    on behalf of one of our donors.

    '''
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False,
    )

    email_address = models.EmailField(
        help_text="Email address of the donor who made this donation.",
    )

    # todo: change these into PositiveIntegerFields
    monthly_amount = models.PositiveSmallIntegerField(
        help_text="Amount to donate each month in cents, not including the tip.",
    )

    tip = models.PositiveSmallIntegerField(
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

