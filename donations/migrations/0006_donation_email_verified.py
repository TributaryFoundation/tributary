# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0005_auto_20161002_2242'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='email_verified',
            field=models.BooleanField(help_text='Whether the email address has been verified by the donor.', default=False),
            preserve_default=False,
        ),
    ]
