# -*- coding: utf-8 -*-
from django.contrib import admin
from polls.models import Poll, Choice


class ChoiceInline(admin.TabularInline):
    """docstring for ChoiceInline."""
    model = Choice
    extra = 0

class PollAdmin(admin.ModelAdmin):
    """docstring for PollAdmin."""
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Date information', {'fields': ['pub_date'], 'classes':['collapse']})
    ]
    inlines = [ChoiceInline]
    list_display = ('name', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question']
    date_hierarchy = 'pub_date'

admin.site.register(Poll, PollAdmin)


admin.site.register(Choice)
