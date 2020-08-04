from django.contrib import admin
from .models import *


# Register your models here.
class InventoryAdmin(admin.ModelAdmin):
    fields = ['user']


admin.site.register(Inventory, InventoryAdmin)


# Register your models here.
class InventoryCardAdmin(admin.ModelAdmin):
    fields = ['inventory', 'name', 'description', 'rarity', 'level', 'maxlevel', 'collected_cards',
              'increase_points_per_level_amount']


admin.site.register(CardItem, InventoryCardAdmin)

# Register your models here.
class AvatarInventoryCardAdmin(admin.ModelAdmin):
    fields = ['inventory', 'name', 'description', 'rarity', 'level', 'maxlevel', 'collected_cards',
              'increase_points_per_level_amount']


admin.site.register(AvatarCardItem, AvatarInventoryCardAdmin)