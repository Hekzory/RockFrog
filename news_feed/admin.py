from django.contrib import admin

from .models import *

class NewsFeedArticlesListAdmin(admin.ModelAdmin):
    fields = ['id', 'list_type', 'articles']
    readonly_fields = ['id']

class BasicCommentsAdmin(admin.ModelAdmin):
    fields = ['id', 'author', 'parent', 'replyto', 'text', 'pluses', 'minuses', 'pubdate']
    readonly_fields = ['id']

class BasicArticleFilesAdmin(admin.ModelAdmin):
    fields = ['id', 'file', 'name', 'files_list']
    readonly_fields = ['id']

class CommentsListAdmin(admin.ModelAdmin):
    fields = ['id']
    readonly_fields = ['id']

class ArticleFilesListAdmin(admin.ModelAdmin):
    fields = ['id']
    readonly_fields = ['id']

class BasicArticlesAdmin(admin.ModelAdmin):
    fields = ['id', 'author', 'title', 'text', 'pubdate', 'pluses', 'minuses', 'comments', 'files', 'rating']
    readonly_fields = ['id']

class PersonalArticlesAdmin(admin.ModelAdmin):
    fields = ['id', 'author', 'title', 'text', 'pubdate', 'pluses', 'minuses', 'comments', 'files', 'rating']
    readonly_fields = ['id']

class PersonalInCommunityArticlesAdmin(admin.ModelAdmin):
    fields = ['id', 'author', 'title', 'group', 'text', 'allowed', 'pubdate', 'pluses', 'minuses', 'comments', 'files', 'rating']
    readonly_fields = ['id']

class CommunityArticlesAdmin(admin.ModelAdmin):
    fields = ['id', 'group', 'title', 'text', 'allowed', 'pubdate', 'pluses', 'minuses', 'comments', 'files', 'rating']   
    readonly_fields = ['id'] 

admin.site.register(NewsFeedArticlesList, NewsFeedArticlesListAdmin)
admin.site.register(BasicComment, BasicCommentsAdmin)
admin.site.register(BasicArticleFile, BasicArticleFilesAdmin)
admin.site.register(CommentsList, CommentsListAdmin)
admin.site.register(ArticleFilesList, ArticleFilesListAdmin)
admin.site.register(BasicArticle, BasicArticlesAdmin)
admin.site.register(PersonalArticle, PersonalArticlesAdmin)
admin.site.register(PersonalInCommunityArticle, PersonalInCommunityArticlesAdmin)
admin.site.register(CommunityArticle, CommunityArticlesAdmin)