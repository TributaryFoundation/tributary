# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0003_auto_20161002_2210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='monthly_amount',
            field=models.PositiveIntegerField(help_text='Amount to donate each month in cents, not including the tip.'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='tip',
            field=models.PositiveIntegerField(help_text='The amount in cents to be given to Tributary Foundation out of each monthly charge.'),
        ),
    ]
