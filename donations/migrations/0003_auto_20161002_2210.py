# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0002_auto_20161002_1954'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='stripe_customer_id',
            field=models.CharField(max_length=1000, help_text='The id of the customer on stripe.', default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='donation',
            name='monthly_amount',
            field=models.PositiveSmallIntegerField(help_text='Amount to donate each month in cents, not including the tip.'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='tip',
            field=models.PositiveSmallIntegerField(help_text='The amount in cents to be given to Tributary Foundation out of each monthly charge.'),
        ),
    ]
