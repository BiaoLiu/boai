# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-11-07 02:39
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boai_model', '0014_auto_20161107_1034'),
    ]

    operations = [
        migrations.AddField(
            model_name='appsalesorders',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='appsendsms',
            name='sms_id',
            field=models.CharField(default='6ae6e682a49311e685dafcaa1469668c', max_length=40, primary_key=True, serialize=False),
        ),
    ]
