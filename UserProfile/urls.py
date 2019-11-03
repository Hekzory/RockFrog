from django.urls import path
from . import views
from .views import ProfileView

app_name = 'UserProfile'

urlpatterns = [
    path('', ProfileView.as_view(), name='index'),
    path('<str:username>/', views.userprofile, name='userprofile'),
]
