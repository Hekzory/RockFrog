from django.urls import path
from . import views
from .views import *

app_name = 'UserProfile'

urlpatterns = [
    path('', ProfileView.as_view(), name='index'),
    path('edit/', EditProfileView.as_view(), name='editprofile'),
    path('edit_privacy/', EditPrivacyView.as_view(), name='edit_privacy'),
    path('<str:username>/', views.userprofile, name='userprofile'),
]
