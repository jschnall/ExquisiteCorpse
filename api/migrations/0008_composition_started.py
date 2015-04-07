# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20150407_1120'),
    ]

    operations = [
        migrations.AddField(
            model_name='composition',
            name='started',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
