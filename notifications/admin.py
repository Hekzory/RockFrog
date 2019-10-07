from django.contrib import admin

from .models import Notification

class NotsAdmin(admin.ModelAdmin):
    fields = ['not_text', 'not_name', 'not_date', 'not_link', 'not_checked']

admin.site.register(Notification, NotsAdmin)