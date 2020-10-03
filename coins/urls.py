from django.urls import path
from .views import *

app_name = 'coins'

urlpatterns = [
    path('', CoinManagementView.as_view(), name='coin_management'),
    path('transactions/', TransactionHistoryView.as_view(), name='transaction_history')
    ]
