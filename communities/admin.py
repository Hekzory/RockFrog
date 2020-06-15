from django.contrib import admin

from .models import *

class GroupsAdmin(admin.ModelAdmin):
    fields = ['groupname', 'slug', 'description', 'image', 'pubdate', 'admin', 'editors', 'subscribers', 'public', 'subrequests', 'banned', 'allowarticles']

class ArticlesAdmin(admin.ModelAdmin):
    fields = ['group', 'text', 'allowed', 'pubdate', 'likes']

class CommentsAdmin(admin.ModelAdmin):
    fields = ['author', 'text', 'pubdate', 'article']

class ArticleFilesAdmin(admin.ModelAdmin):
    fields = ['article', 'file', 'name']

class GroupFilesAdmin(admin.ModelAdmin):
    fields = ['group', 'file']

class GroupImagesAdmin(admin.ModelAdmin):
    fields = ['group', 'image']

admin.site.register(Group, GroupsAdmin)
admin.site.register(GroupArticle, ArticlesAdmin)
admin.site.register(GroupComment, CommentsAdmin)
admin.site.register(ArticleFile, ArticleFilesAdmin)
admin.site.register(GroupFile, GroupFilesAdmin)