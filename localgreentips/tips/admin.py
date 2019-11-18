from django.contrib import admin

from .models import Tip, Comment


class TipAdmin(admin.ModelAdmin):
    search_fields = ('cities__name', 'subregions__name',
                     'regions__name', 'countries__name')


admin.site.register(Tip, TipAdmin)
admin.site.register(Comment)
