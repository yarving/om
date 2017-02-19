# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.utils import timezone
from django.db import models


class Officer(models.Model):
    """docstring for Pool."""
    name = models.CharField('姓名', max_length=200)
    pub_date = models.DateTimeField('更新日期')

    def __str__(self):
        return self.name

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=7)

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = '是否近期更新?'


class Choice(models.Model):
    """docstring for Choice."""
    officer = models.ForeignKey(Officer)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField()

    def __str__(self):
        return self.choice
