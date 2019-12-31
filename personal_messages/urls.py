from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.DialogsList.as_view(), name='conversations'),
    path('user/<int:user_id>', views.DialogPage.as_view(), name='conversation')
]