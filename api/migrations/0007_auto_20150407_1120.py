# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20150406_1846'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='composition',
            name='complete',
        ),
        migrations.AddField(
            model_name='composition',
            name='completed',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='composition',
            name='max_part_chars',
            field=models.IntegerField(default=500),
        ),
        migrations.AlterField(
            model_name='composition',
            name='max_users',
            field=models.IntegerField(default=2),
        ),
        migrations.AlterField(
            model_name='composition',
            name='min_part_chars',
            field=models.IntegerField(default=1),
        ),
    ]
