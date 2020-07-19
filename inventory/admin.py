from django.contrib import admin
from .models import *


# Register your models here.
class InventoryAdmin(admin.ModelAdmin):
    fields = ['user']


admin.site.register(Inventory, InventoryAdmin)


# Register your models here.
class InventoryCardAdmin(admin.ModelAdmin):
    fields = ['inventory', 'name', 'description', 'rarity']


admin.site.register(CardItem, InventoryCardAdmin)