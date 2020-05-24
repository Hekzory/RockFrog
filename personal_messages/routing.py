from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    path('ws/personal_messages/<int:user_id>', consumers.PMConsumer),
    path('ws/dialog_list', consumers.DialogListConsumer),
]