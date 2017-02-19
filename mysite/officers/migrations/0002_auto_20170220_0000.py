# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-19 16:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('officers', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='officer',
            options={'verbose_name': '\u5e72\u90e8', 'verbose_name_plural': '\u5e72\u90e8'},
        ),
        migrations.AddField(
            model_name='officer',
            name='gender',
            field=models.CharField(choices=[('\u7537', '\u7537'), ('\u5973', '\u5973')], default='\u7537', max_length=2, verbose_name='\u6027\u522b'),
        ),
        migrations.AlterField(
            model_name='officer',
            name='name',
            field=models.CharField(max_length=20, verbose_name='\u59d3\u540d'),
        ),
    ]
