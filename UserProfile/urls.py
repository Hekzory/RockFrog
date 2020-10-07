from django.urls import path
from . import views
from .views import *

app_name = 'UserProfile'

urlpatterns = [
    path('', YourProfileView.as_view(), name='index'),
    path('settings/', ProfileSettings.as_view(), name='profile_settings'),
    path('edit/', EditProfileView.as_view(), name='editprofile'),
    path('settings/blockedusers/', BlockedUsersView.as_view(), name='blockedusers'),
    path('settings/edit_privacy/', EditPrivacyView.as_view(), name='edit_privacy'),
    path('settings/edit_security/', EditSecurityView.as_view(), name='edit_security'),
    path('settings/edit_notifications/', EditNotificationsView.as_view(), name='edit_notifications'),
    path('block/', BlockUserView.as_view(), name='block_user'),
    path('unblock/', UnblockUserView.as_view(), name='unblock_user'),
    path('update_rating/', update_rating, name='update_rating'),
    path('get_posts/', GetPosts.as_view(), name='get_posts'),
    path('<str:username>/', UserProfileView.as_view(), name='userprofile'),
]
