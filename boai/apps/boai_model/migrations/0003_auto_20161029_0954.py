# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-29 01:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boai_model', '0002_auto_20161029_0952'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appsocialprice',
            old_name='social_id',
            new_name='id',
        ),
        migrations.AlterField(
            model_name='appsendsms',
            name='sms_id',
            field=models.CharField(default='96b890869d7a11e6833d047d7b6f978e', max_length=40, primary_key=True, serialize=False),
        ),
    ]