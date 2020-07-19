from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Inventory(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username+"'s inventory"


class InventoryItem(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    name = models.TextField(default="Standart item name")
    description = models.TextField(default="Standart item description")
    type = models.TextField(default="abstract")

    class Meta:
        abstract = True


class CardItem(InventoryItem):
    name = models.TextField(default="Standart card name")
    description = models.TextField(default="Standart card description")
    rarity = models.TextField(default="common")
    type = models.TextField(default="card")
