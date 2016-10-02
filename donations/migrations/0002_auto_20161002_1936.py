# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='id',
            field=models.UUIDField(serialize=False, primary_key=True, editable=False, default=uuid.uuid4),
        ),
    ]
