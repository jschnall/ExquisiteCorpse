# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_composition_complete'),
    ]

    operations = [
        migrations.AddField(
            model_name='composition',
            name='complete',
            field=models.BooleanField(default=False),
        ),
    ]
