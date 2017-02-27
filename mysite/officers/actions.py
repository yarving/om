#!/usr/bin/env python
# encoding: utf-8


import csv
import time
from django.http import HttpResponse


def export_as_csv_action(description="导出为CSV文件",
                         fields=None, exclude=None, header=True):
    """
    This function returns an export csv action
    'fields' and 'exclude' work like in django ModelForm
    'header' is whether or not to output the column names as the first row
    """
    def export_as_csv(modeladmin, request, queryset):
        """
        Generic csv export admin action.
        based on http://djangosnippets.org/snippets/1697/
        """
        opts = modeladmin.model._meta

        field_names = [field.name for field in opts.fields]
        field_maps = {field.name: field.verbose_name for field in opts.fields}
        if fields:
            # fieldset = set(fields)
            # field_names = field_names & fieldset
            field_list = list(fields)
            field_names = field_list
        elif exclude:
            excludeset = set(exclude)
            field_names = field_names - excludeset

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=info-{}.csv'.format(time.strftime('%Y-%m-%d-%H-%M-%S'))

        writer = csv.writer(response)
        if header:
            # writer.writerow(list(field_names))
            writer.writerow([field_maps[x] for x in field_names])
        for obj in queryset:
            writer.writerow([(getattr(obj, field)) for field in field_names])
        return response
    export_as_csv.short_description = description
    return export_as_csv
