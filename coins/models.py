from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from UserProfile.models import *
from datetime import datetime, timedelta


class CoinManagement(models.Model):
    coins = models.IntegerField(default=0)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.profile)+'_coin_management'


class Transaction(models.Model):
    type = models.TextField(blank=False)
    amount = models.IntegerField(blank=False)
    sender = models.TextField(blank=False)
    receiver = models.TextField(blank=False)
    coin_management = models.ForeignKey(CoinManagement, on_delete=models.CASCADE)
    time_created = models.DateTimeField(default=datetime.now)

    def __str__(self):
        time = self.time_created + timedelta(hours=3)
        name = str(self.sender)+'-'+str(self.receiver)
        if self.amount >= 0:
            name = name+'|'+'+'+str(self.amount)+'|'
        else:
            name = name+'|'+str(self.amount)+'|'
        name = name+time.strftime("%m/%d/%Y, %H:%M:%S")
        return name


@receiver(post_save, sender=Profile)
def create_coin_management(sender, instance, created, **kwargs):
    if created:
        CoinManagement.objects.create(profile=instance)
