from django.urls import path
from . import views
from .views import *

app_name = 'news'

urlpatterns = [
    path('', NewsListView.as_view(), name='index'),
    path('<int:news_id>/', views.news_post, name='news_post'),
]
