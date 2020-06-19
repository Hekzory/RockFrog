from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.DialogsList.as_view(), name='conversations'),
    path('base_list', views.DialogsListBase.as_view(), name='base_list'),
    path('user/<int:user_id>', views.DialogPage.as_view(), name='conversation'),
    path('delete_message', views.DeleteMessage.as_view(), name='delete_message'),
    path('edit_message', views.EditMessage.as_view(), name='edit_message'),
]