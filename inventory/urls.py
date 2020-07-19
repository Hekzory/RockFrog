from django.urls import path
from .views import *

app_name = 'inventory'

urlpatterns = [
    path('', MyInventoryView.as_view(), name='index'),
    path('get_item/', GetItemView.as_view(), name='index'),
]