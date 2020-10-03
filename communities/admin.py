from django.contrib import admin

from .models import *

class GroupsAdmin(admin.ModelAdmin):
    fields = ['groupname', 'slug', 'description', 'image', 'pubdate', 'admin', 'editors', 'subscribers', 'public', 'subrequests', 'banned', 'allowarticles']

class GroupFilesAdmin(admin.ModelAdmin):
    fields = ['group', 'file']

admin.site.register(Group, GroupsAdmin)
admin.site.register(GroupFile, GroupFilesAdmin)