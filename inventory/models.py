from django.db import models
from django.contrib.auth.models import User
from model_utils.managers import InheritanceManager


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
    next_level_descriptions = []
    name = models.TextField(default="Standart card name")
    description = models.TextField(default="Standart card description")
    rarity = models.TextField(default="common")
    type = models.TextField(default="card")
    level = models.IntegerField(default=0)
    maxlevel = models.IntegerField()
    collected_cards = models.IntegerField(default=0)
    increase_points_per_level_amount = models.IntegerField(default=2)
    objects = InheritanceManager()

    def add_cards(self, amount):
        self.collected_cards += amount
        self.save()

    def increase_level(self):
        if (self.collected_cards >= (self.level+1)*self.increase_points_per_level_amount) and self.level < self.maxlevel:
            self.level += 1
            self.collected_cards -= self.level*self.increase_points_per_level_amount
            self.save()
            return self.maxlevel
        else:
            return None

    def get_next_level_descriptions(self):
        return []

    def get_next_level_description(self):
        try:
            return self.next_level_descriptions[self.level+1]
        except:
            return "Описание отсутствует"

    def get_improvable_stats_list(self):
        return []


class AvatarCardItem(CardItem):
    next_level_descriptions = ['Базовый уровень карточки.', 'Увеличение максимального разрешения до 512x512',
                               'Увеличение максимального размера до 1 МБ', 'Увеличение максимального разрешения до 1024x1024',
                               'Увеличение максимального размера до 3 МБ', 'Увеличение максимального разрешения до 2048x2048',
                               'Увеличение максимального размера до 5 МБ', 'Возможность использовать GIF']

    # Возвращает максимальное разрешение аватара в пикселях
    def get_max_resolution(self):
        if self.level >= 5:
            return 2048, 2048
        if self.level >= 3:
            return 1024, 1024
        if self.level >= 1:
            return 512, 512
        return 256, 256

    # Возвращает максимальный размер аватара в Мегабайтах
    def get_max_size(self):
        if self.level >= 6:
            return 5
        if self.level >= 4:
            return 3
        if self.level >= 2:
            return 1
        return 0.5

    # Проверка возможности ставить GIF на аватарку
    def is_gif_enabled(self):
        return self.level >= 7

    # Вернуть список пар, содержащих описание характеристик, которые возможно прокачать
    def get_improvable_stats_list(self):
        gif_enabled = "Нет"
        if self.is_gif_enabled():
            gif_enabled = "Есть"
        return ('Максимальное разрешение:', '{}x{}'.format(*self.get_max_resolution())), \
               ('Максимальный размер:', '{} МБ'.format(self.get_max_size())), \
               ('Возможность использовать GIF:', gif_enabled)


