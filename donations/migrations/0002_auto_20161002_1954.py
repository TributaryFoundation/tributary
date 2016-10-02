# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='tip',
            field=models.PositiveSmallIntegerField(help_text='The amount in whole dollars to be given to Tributary Foundation out of each monthly charge.', default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='donation',
            name='monthly_amount',
            field=models.PositiveSmallIntegerField(help_text='Amount to donate each month in whole dollars, including the tip.'),
        ),
    ]
