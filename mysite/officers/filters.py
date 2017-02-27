#!/usr/bin/env python
# encoding: utf-8


import datetime
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class PromotionFilter(admin.SimpleListFilter):
    title = _('是否可提拔')
    parameter_name = 'promotion'

    def lookups(self, request, model_admin):
        return (
            ('y', _('可提拔')),
            ('n', _('不可提拔')),
        )

    def queryset(self, request, queryset):
        today = datetime.datetime.now().date()
        if self.value() == 'y':
            return queryset.exclude(forbidden_start__lte=today, forbidden_end__gte=today)
            return queryset.filter((forbidden_start is None) or
                                   (forbidden_end is None) or
                                   (forbidden_start>today) or
                                   (forbidden_end__lt<today))
        elif self.value() == 'n':
            return queryset.filter(forbidden_start__lte=today, forbidden_end__gte=today)
