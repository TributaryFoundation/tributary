from django.db import models


class Donation(models.Model):
    '''A Donation represents a single submitted instruction to donations
    on behalf of one of our donors.

    '''
    email_address = models.EmailField(help_text="Email address of the donor who made this donation.")
    monthly_amount = models.PositiveSmallIntegerField(help_text="Amount to donate each month in whole dollars.")
    instructions = models.TextField(help_text="The unstructured instructions describing where the donation should be sent.")
    donor_name = models.CharField(help_text="When making a donation, do it on behalf of this name.", max_length=1000)

    # TODO: stripe customer ID:
    # stripe_customer_id = models.CharField()
