# -*- coding: utf-8 -*-
from django.contrib import admin

from officers.models import Officer, Choice, Assessment, PersonalEvent, \
    EconomicReview, PetitionReport, OrganizeProcess, PartyAffair, VetoAffair
from officers.actions import export_as_csv_action


class ChoiceInline(admin.TabularInline):
    """docstring for ChoiceInline."""
    model = Choice
    extra = 0


class AssessmentInline(admin.StackedInline):
    """年度考核"""
    model = Assessment
    classes = ['collapse']
    extra = 0


class PersonalEventInline(admin.StackedInline):
    """个人事项报告"""
    model = PersonalEvent
    classes = ['collapse']
    extra = 0


class EconomicReviewInline(admin.StackedInline):
    """"""
    model = EconomicReview
    classes = ['collapse']
    extra = 0


class PetitionReportInline(admin.StackedInline):
    """"""
    model = PetitionReport
    classes = ['collapse']
    extra = 0


class OrganizeProcessInline(admin.StackedInline):
    """"""
    model = OrganizeProcess
    classes = ['collapse']
    extra = 0


class PartyAffairInline(admin.TabularInline):
    """"""
    model = PartyAffair
    classes = ['collapse']
    extra = 0


class VetoAffairInline(admin.TabularInline):
    """"""
    model = VetoAffair
    classes = ['collapse']
    extra = 0


class OfficerAdmin(admin.ModelAdmin):
    """docstring for PollAdmin."""
    fieldsets = [
        (None, {'fields': ['name']}),
        ('个人基本信息',
         {'fields': ['gender', 'birthday', 'is_party', 'party_time', 'job_time',
                     'native', 'nation', 'duty_level', 'id_number',
                     'full_time_edu', 'full_time_deg',
                     'part_time_edu', 'part_time_deg', 'forbidden_start', 'forbidden_end',
                     'job_title', 'pub_date'],
          'classes':['collapse']}),
    ]
    inlines = [AssessmentInline, PersonalEventInline, EconomicReviewInline,
               PetitionReportInline, OrganizeProcessInline,
               PartyAffairInline, VetoAffairInline]
    list_display = ('name', 'gender', 'birthday', 'is_party', 'party_time',
                    'job_time', 'native', 'nation', 'duty_level',
                    'job_title', 'pub_date', 'was_able_promotion')
    from officers.filters import PromotionFilter
    list_filter = ['pub_date', PromotionFilter]
    search_fields = ['name']
    date_hierarchy = 'pub_date'
    actions = [ export_as_csv_action( "导出",), ]

# register Officer page
admin.site.register(Officer, OfficerAdmin)

# register others can be displayed on home page
admin.site.register(PersonalEvent)
admin.site.register(EconomicReview)
admin.site.register(PetitionReport)
admin.site.register(OrganizeProcess)
admin.site.register(PartyAffair)
admin.site.register(VetoAffair)
