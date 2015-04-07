# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Composition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('max_users', models.IntegerField(default=2, blank=True)),
                ('title', models.CharField(max_length=100, blank=True)),
                ('turns', models.IntegerField(default=1, blank=True)),
                ('min_part_chars', models.IntegerField(default=1, blank=True)),
                ('max_part_chars', models.IntegerField(default=500, blank=True)),
                ('join_policy', models.CharField(default=b'OPEN', max_length=100, choices=[(b'OPEN', b'Open'), (b'INVITE_ONLY', b'Invite only')])),
                ('public_result', models.BooleanField(default=True)),
                ('complete', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(related_name='composition_users', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('text', models.TextField(max_length=10000, blank=True)),
                ('segue', models.CharField(max_length=100, blank=True)),
                ('composition', models.ForeignKey(to='api.Composition')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('owner', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
