# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.utils import timezone
from django.db import models


class Officer(models.Model):
    """docstring for Pool."""
    name = models.CharField('姓名', max_length=20)
    pub_date = models.DateTimeField('更新日期')
    gender_choices = (
        ('男', '男'),
        ('女', '女'),
    )
    birthday = models.DateField('出生日期')
    gender = models.CharField('性别', max_length=2,
                              choices=gender_choices,
                              default='男')
    native = models.CharField('籍贯', max_length=20, default='湖南永州')
    nation = models.CharField('民族', max_length=20, default='汉')
    duty_level = models.CharField('职务层次', max_length=20, default='无')
    id_number = models.CharField('身份证号', max_length=18, default='无')

    def __str__(self):
        return self.name

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=7)

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = '是否近期更新?'

    class Meta:
        verbose_name = '干部'
        verbose_name_plural = '干部'


class Choice(models.Model):
    """docstring for Choice."""
    officer = models.ForeignKey(Officer)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField()

    def __str__(self):
        return self.choice
