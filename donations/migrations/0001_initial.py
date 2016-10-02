# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, editable=False)),
                ('email_address', models.EmailField(max_length=254, help_text='Email address of the donor who made this donation.')),
                ('monthly_amount', models.PositiveSmallIntegerField(help_text='Amount to donate each month in whole dollars.')),
                ('instructions', models.TextField(help_text='The unstructured instructions describing where the donation should be sent.')),
                ('donor_name', models.CharField(max_length=1000, help_text='When making a donation, do it on behalf of this name.')),
            ],
        ),
    ]
