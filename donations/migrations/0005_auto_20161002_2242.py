# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0004_auto_20161002_2228'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 2, 22, 41, 51, 883112, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='donation',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 2, 22, 42, 0, 107670, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
