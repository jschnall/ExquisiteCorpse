__author__ = 'jschnall'

from django.contrib import admin

from models import *


class CompositionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'join_policy', 'owner')


class PartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'segue', 'owner')


admin.site.register(Composition, CompositionAdmin)
admin.site.register(Part, PartAdmin)
