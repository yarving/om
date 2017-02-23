# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-20 14:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('officers', '0004_auto_20170220_2135'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(choices=[('2016', '2016'), ('2015', '2015'), ('2014', '2014')], default='2017', max_length=4, verbose_name='年度')),
                ('level', models.CharField(choices=[('优秀', '优秀'), ('称职', '称职'), ('基本称职', '基本称职'), ('不称职', '不称职')], default='优秀', max_length=8, verbose_name='评定等级')),
                ('Officer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='officers.Officer')),
            ],
            options={
                'verbose_name_plural': '年度考核',
                'verbose_name': '年度考核',
            },
        ),
    ]