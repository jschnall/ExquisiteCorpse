# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_composition_complete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='composition',
            name='title',
            field=models.CharField(unique=True, max_length=100),
        ),
    ]
