# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-11 15:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppStock',
            fields=[
                ('pk_stock', models.CharField(max_length=40, primary_key=True, serialize=False, verbose_name='股票代码')),
                ('stockname', models.CharField(blank=True, max_length=100, null=True, verbose_name='股票名称')),
                ('tradetype', models.CharField(blank=True, max_length=100, null=True, verbose_name='股票类型')),
                ('isdisabled', models.NullBooleanField(verbose_name='是否启用')),
                ('istop', models.NullBooleanField(verbose_name='是否置顶')),
                ('sortno', models.IntegerField(blank=True, null=True, verbose_name='排序号')),
                ('createtime', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '股票',
                'db_table': 'app_stock',
                'verbose_name_plural': '股票列表',
            },
        ),
    ]
