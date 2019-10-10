from datetime import datetime
from django.contrib.auth.models import User
from chat.models import Chat
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


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
		notification = Notification.objects.create(not_text = 'Test 4', not_name = 'Test 4', not_link = '/')	

		notificationlist = Notificationlist.objects.get(user = User.objects.get(id = 1))
		print(notificationlist)

		# for user_to_send in User.objects.all():
			# if user_to_send != Chat.objects.all()[::-1][0].user:
				# print(user_to_send)
				# notification = Notification()
				# notification.not_text = 'test2'
				# notification.not_name = 'test2'
				# notification.not_link = '/'
				# print(notification)
				# notification.save()
				
