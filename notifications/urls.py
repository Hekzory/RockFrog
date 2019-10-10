from django.urls import path
from . import views
from .views import *

app_name = 'notifications'

urlpatterns = [
    path('', NotificationsList.as_view(), name='index'),
    path('check/', NotificationsList.as_view(), name='check'),
]
