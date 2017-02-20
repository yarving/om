# -*- coding: utf-8 -*-
from django.contrib import admin
from officers.models import Officer, Choice, Assessment, PersonalEvent


class ChoiceInline(admin.TabularInline):
    """docstring for ChoiceInline."""
    model = Choice
    extra = 0


class AssessmentInline(admin.TabularInline):
    """年度考核"""
    model = Assessment
    classes = ['collapse']
    extra = 0


class PersonalEventInline(admin.TabularInline):
    """年度考核"""
    model = PersonalEvent
    classes = ['collapse']
    extra = 0


class OfficerAdmin(admin.ModelAdmin):
    """docstring for PollAdmin."""
    fieldsets = [
        (None, {'fields': ['name']}),
        ('个人基本信息',
         {'fields': ['gender', 'birthday', 'party_time', 'job_time',
                     'native', 'nation', 'duty_level', 'id_number',
                     'full_time_edu', 'full_time_deg',
                     'part_time_edu', 'part_time_deg',
                     'job_title', 'manage_field', 'profile',
                     'pub_date'],
          'classes':['collapse']}),
    ]
    inlines = [AssessmentInline, PersonalEventInline]
    list_display = ('name', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['name']
    date_hierarchy = 'pub_date'

# register Officer page
admin.site.register(Officer, OfficerAdmin)

# register others can be displayed on home page
admin.site.register(PersonalEvent)
