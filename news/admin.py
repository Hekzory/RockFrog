from django.contrib import admin

from .models import Post

class PostsAdmin(admin.ModelAdmin):
    fields = ['post_name', 'post_announce', 'post_text', 'post_date']

admin.site.register(Post, PostsAdmin)
