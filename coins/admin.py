from django.contrib import admin
from .models import CoinManagement, Transaction


class CoinManagementAdmin(admin.ModelAdmin):
    fields = ['coins', 'profile']
    empty_value_display = 'Не указано'


class TransactionAdmin(admin.ModelAdmin):
    fields = ['type', 'amount', 'sender', 'receiver', 'coin_management']
    empty_value_display = 'Не указано'


admin.site.register(CoinManagement, CoinManagementAdmin)
admin.site.register(Transaction, TransactionAdmin)
