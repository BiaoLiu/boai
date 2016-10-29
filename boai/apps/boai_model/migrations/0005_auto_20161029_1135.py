# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-29 03:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boai_model', '0004_auto_20161029_0954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appsendsms',
            name='sms_id',
            field=models.CharField(default='bdd0dcc29d8811e68f92047d7b6f978e', max_length=40, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='appsocialprice',
            name='disability',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True),
        ),
        migrations.AlterField(
            model_name='appsocialprice',
            name='employment',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True),
        ),
        migrations.AlterField(
            model_name='appsocialprice',
            name='endowment',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True),
        ),
        migrations.AlterField(
            model_name='appsocialprice',
            name='housingfund',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True),
        ),
        migrations.AlterField(
            model_name='appsocialprice',
            name='maternity',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True),
        ),
        migrations.AlterField(
            model_name='appsocialprice',
            name='medical',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True),
        ),
        migrations.AlterField(
            model_name='appsocialprice',
            name='unemployment',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True),
        ),
    ]
