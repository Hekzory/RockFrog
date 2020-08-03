from django.urls import path
from .views import *
from django.conf import settings

app_name = 'news_feed'

urlpatterns = [
    path('', home, name='home'),
    path('manage_comments/', manage_comments, name='manage_comments'),
    path('manage_articles/', manage_articles, name='manage_articles'),
    path('manage_settings/', manage_settings, name='manage_settings'),
    path('<int:articleid>/', view_article, name='view_article'),   
]