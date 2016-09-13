# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-13 03:18
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boai_model', '0002_appsendsms'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppPlatformUser',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('nickname', models.CharField(blank=True, max_length=40, null=True)),
                ('avatar', models.CharField(blank=True, max_length=200, null=True)),
                ('platform', models.CharField(blank=True, max_length=20, null=True)),
                ('openid', models.CharField(blank=True, max_length=40, null=True)),
                ('access_token', models.CharField(blank=True, max_length=40, null=True)),
                ('refresh_token', models.CharField(blank=True, max_length=40, null=True)),
                ('expirationtime', models.DateTimeField(blank=True, null=True)),
                ('profileurl', models.CharField(blank=True, max_length=200, null=True)),
                ('ts', models.DateTimeField(blank=True, null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'app_platform_user',
            },
        ),
    ]