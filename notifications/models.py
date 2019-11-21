from datetime import datetime
from django.contrib.auth.models import User
from chat.models import Chat
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.html import strip_tags
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class Notification(models.Model):
    not_text = models.TextField()
    not_name = models.CharField(max_length=100)
    not_date = models.DateTimeField('date published', default=datetime.now())
    not_link = models.CharField(max_length=200)
    not_checked = models.BooleanField(default=True)
    def __str__(self):
        return self.not_name
    def unchecked(self):
        return self.not_checked == True

class Notificationlist(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	notifications = models.ManyToManyField(Notification)
	def __str__(self):
	    return self.user.username

@receiver(post_save, sender=User)
def create_user_NotificationList(sender, instance, created, **kwargs):
    if created:
        Notificationlist.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_NotificationList(sender, instance, **kwargs):
    instance.notificationlist.save()

@receiver(post_save, sender=Chat)
def create_Notification(sender, instance, created, **kwargs):
    if created:
        notification_text = strip_tags(str(instance.message))
        notification_name = strip_tags(str(instance.user.username)+': новое сообщение')
        notification = Notification.objects.create(not_text = notification_text, not_name = notification_name, not_link = '/')
        notification.save()
        print(notification.not_name, notification.not_text)
        notificationlist = Notificationlist.objects.get(user = User.objects.get(id = instance.user.id)).notifications
        notificationlist.add(notification)

        channel_layer = get_channel_layer()
        print("Trying to send message for "+"notifications_"+User.objects.get(id = instance.user.id).username)
        async_to_sync(channel_layer.group_send)("notifications_"+User.objects.get(id = instance.user.id).username, {"type": "notification", "message": notification_text, "header": notification_name})
