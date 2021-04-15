from django.urls import path
from .views import *

app_name = 'news_feed'

urlpatterns = [
    path('', ViewArticles.as_view(), name='home'),
    path('get_posts/', GetPosts.as_view(), name='get_posts'),
    path('manage_comments/', manage_comments, name='manage_comments'),
    path('manage_articles/', manage_articles, name='manage_articles'),
    path('manage_settings/', manage_settings, name='manage_settings'),
    path('article/<int:articleid>/', view_article, name='view_article'),
]