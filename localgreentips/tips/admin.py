from django.contrib import admin

from .models import Tipper, Tip, Comment

admin.site.register(Tip)
admin.site.register(Tipper)
admin.site.register(Comment)
