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
def create_Notification_onchat(sender, instance, created, **kwargs):
    if created:
        notification_text = strip_tags(str(instance.message))
        notification_name = strip_tags(str(instance.user.username)+' написал в чат')
        notification_href = '/chat'
        notification = Notification.objects.create(not_text = notification_text, not_name = notification_name, not_link = notification_href)
        notification.save()
        notificationlist = Notificationlist.objects.get(user = User.objects.get(id = instance.user.id)).notifications
        notificationlist.add(notification)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)("notifications_"+User.objects.get(id = instance.user.id).username, {"type": "notification", "message": notification_text, "header": notification_name, "href": notification_href})

def create_notification_on_pm(from_user, to_user):
    notification_text = "Вам пришло новое сообщение от "+from_user.username
    notification_name = "Новое сообщение"
    notification_href = '/conversations'
    notification = Notification.objects.create(not_text = notification_text, not_name = notification_name, not_link = notification_href)
    notification.save()
    notificationlist = Notificationlist.objects.get(user=User.objects.get(id=to_user.id)).notifications
    notificationlist.add(notification)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)("notifications_" + User.objects.get(id=to_user.id).username,
                                            {"type": "notification", "message": notification_text,
                                             "header": notification_name, "href": notification_href})

def create_notification_post_published(group, to_user, notification_type):
    flag = False
    if notification_type == 'post_accepted':
        notification_text = "Ваш пост в " + group.groupname + " опубликован"
        notification_name = "Пост опубликован"
        notification_href = '/groups/' + group.slug + '/'
        flag = True
    elif notification_type == 'post_rejected':
        notification_text = "Ваш пост в " + group.groupname + " отклонен"
        notification_name = "Пост отклонен"
        notification_href = '/groups/' + group.slug + '/'
        flag = True
    elif notification_type == 'post_deleted':
        notification_text = "Ваш пост в " + group.groupname + " удален"
        notification_name = "Пост удален"
        notification_href = '/groups/' + group.slug + '/'  
        flag = True

    if flag: 
        notification = Notification.objects.create(not_text = notification_text, not_name = notification_name, not_link = notification_href)
        notification.save()
        notificationlist = Notificationlist.objects.get(user=User.objects.get(id=to_user.id)).notifications
        notificationlist.add(notification)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)("notifications_" + User.objects.get(id=to_user.id).username,
                                                {"type": "notification", "message": notification_text,
                                                 "header": notification_name, "href": notification_href})

def create_notification_accepted_to_group(group, to_user, notification_type):
    flag = False
    if notification_type == 'request_accepted':
        notification_text = "Ваша заявка в " + group.groupname + " принята"
        notification_name = "Заявка принята"
        notification_href = '/groups/' + group.slug + '/'
        flag = True
    elif notification_type == 'request_rejected':
        notification_text = "Ваша заявка в " + group.groupname + " отклонена"
        notification_name = "Заявка отклонена"
        notification_href = '/groups/' + group.slug + '/'
        flag = True
    elif notification_type == 'banned':
        notification_text = "Вас добавили в черный список ообщества " + group.groupname
        notification_name = "Вас заблокировали"
        notification_href = '/groups/' + group.slug + '/'
        flag = True
    elif notification_type == 'restored':
        notification_text = "Вас убрали из черного списка ообщества " + group.groupname
        notification_name = "Вас разблокировали"
        notification_href = '/groups/' + group.slug + '/'
        flag = True
    elif notification_type == 'promoted':
        notification_text = "Вас повысили до редактора в сообществе " + group.groupname
        notification_name = "Вас повысили"
        notification_href = '/groups/' + group.slug + '/'
        flag = True
    elif notification_type == 'demoted':
        notification_text = "Вас понизили до участника в сообществе " + group.groupname
        notification_name = "Вас понизили"
        notification_href = '/groups/' + group.slug + '/'
        flag = True
    elif notification_type == 'to_admin':
        notification_text = "Вас повысили до администратора в сообществе " + group.groupname
        notification_name = "Вас повысили"
        notification_href = '/groups/' + group.slug + '/'
        flag = True

    if flag: 
        notification = Notification.objects.create(not_text = notification_text, not_name = notification_name, not_link = notification_href)
        notification.save()
        notificationlist = Notificationlist.objects.get(user=User.objects.get(id=to_user.id)).notifications
        notificationlist.add(notification)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)("notifications_" + User.objects.get(id=to_user.id).username,
                                                {"type": "notification", "message": notification_text,
                                                 "header": notification_name, "href": notification_href})