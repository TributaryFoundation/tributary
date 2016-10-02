# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('email_address', models.EmailField(help_text='Email address of the donor who made this donation.', max_length=254)),
                ('monthly_amount', models.PositiveSmallIntegerField(help_text='Amount to donate each month in whole dollars.')),
                ('instructions', models.TextField(help_text='The unstructured instructions describing where the donation should be sent.')),
                ('donor_name', models.CharField(help_text='When making a donation, do it on behalf of this name.', max_length=1000)),
            ],
        ),
    ]
