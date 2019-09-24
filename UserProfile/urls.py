from django.urls import path
from . import views

app_name = 'UserProfile'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:username>/', views.userprofile, name='userprofile'),
]
