from django.urls import path
from . import views
from .views import *

app_name = 'UserProfile'

urlpatterns = [
    path('', YourProfileView.as_view(), name='index'),
    path('edit/', EditProfileView.as_view(), name='editprofile'),
    path('blockedusers/', BlockedUsersView.as_view(), name='blockedusers'),
    path('edit_privacy/', EditPrivacyView.as_view(), name='edit_privacy'),
    path('<str:username>/block/', BlockUserView.as_view(), name='block_user'),
    path('<str:username>/unblock/', UnblockUserView.as_view(), name='unblock_user'),
    path('<str:username>/', UserProfileView.as_view(), name='userprofile'),
]
