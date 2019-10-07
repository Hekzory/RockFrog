from django.contrib import admin

from .models import Notification, Notificationlist

class NotsAdmin(admin.ModelAdmin):
    fields = ['not_text', 'not_name', 'not_date', 'not_link', 'not_checked']

admin.site.register(Notification, NotsAdmin)
admin.site.register(Notificationlist)