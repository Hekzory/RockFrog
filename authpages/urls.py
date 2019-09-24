from django.urls import path
from . import views
from .views import *

urlpatterns = [
    #path('login/', views.index, name='login'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', views.logoutview, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]
