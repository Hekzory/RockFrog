from django.contrib import admin

from .models import *


class DialogListAdmin(admin.ModelAdmin):
    fields = ['user', 'dialogs']


admin.site.register(DialogList, DialogListAdmin)


class DialogAdmin(admin.ModelAdmin):
    fields = ['owner', 'user', 'messages', 'last_view']


admin.site.register(Dialog, DialogAdmin)


class DialogMessageAdmin(admin.ModelAdmin):
    fields = ['user', 'text', 'date_time']


admin.site.register(DialogMessage, DialogMessageAdmin)
