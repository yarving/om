# -*- coding: utf-8 -*-
from django.contrib import admin
from officers.models import Officer, Choice


class ChoiceInline(admin.TabularInline):
    """docstring for ChoiceInline."""
    model = Choice
    extra = 0


class OfficerAdmin(admin.ModelAdmin):
    """docstring for PollAdmin."""
    fieldsets = [
        (None, {'fields': ['name']}),
        ('个人基本信息',
         {'fields': ['birthday', 'gender', 'native', 'nation', 'duty_level', 'id_number',
                     'pub_date'],
          'classes':['collapse']})
    ]
    inlines = [ChoiceInline]
    list_display = ('name', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['name']
    date_hierarchy = 'pub_date'

admin.site.register(Officer, OfficerAdmin)

admin.site.register(Choice)
