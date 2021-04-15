from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.html import strip_tags
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import os
from django.db.models import Q


class Group(models.Model):
	groupname = models.CharField(max_length=40)
	image = models.ImageField(upload_to='groups/groupimages', default=False)
	slug = models.SlugField(max_length=40, unique=True)
	description = models.TextField(blank=True)
	public = models.BooleanField(default=True)
	allowarticles = models.IntegerField(default=2)
	pubdate = models.DateTimeField('date published', default=datetime.now)
	admin = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='groups_admins')
	editors = models.ManyToManyField(User, blank=True, related_name='groups_editors')
	subscribers = models.ManyToManyField(User, blank=True, related_name='groups_subs')
	subrequests = models.ManyToManyField(User, blank=True, related_name='groups_requests')
	banned = models.ManyToManyField(User, blank=True, related_name='groups_banned')

	rating = models.FloatField(null=True, blank=True, default=0)

	def __str__(self):
		return self.groupname

	def has_power(self, user):
		print(user, self.admin, self)
		return user in self.editors.all() or user == self.admin

	def can_see_group(self, user):
		if self.public:
			return True
		if not user.is_authenticated:
			return False
		if user in self.subscribers.all() or user in self.editors.all() or user == self.admin:
			return True
		return False

	def subscribe(self, user):
		user.profile.last_online_update()	
		if self.can_see_group(user) and user not in self.subscribers.all() and user not in self.editors.all() and user != self.admin:
			self.subscribers.add(user)
			self.save()

	def unsubscribe(self, user):
		user.profile.last_online_update()	
		if user in self.editors.all():
			self.editors.remove(user)
			self.save()
		elif user in self.subscribers.all():
			self.subscribers.remove(user)
			self.save()

	def send_subrequest(self, user):
		user.profile.last_online_update()	
		if not self.public and user not in self.subscribers.all() and user not in self.editors.all() and user != self.admin and user not in self.banned.all():
			self.subrequests.add(user)
			self.save()

	def cancel_subrequest(self, user):
		user.profile.last_online_update()	
		if user in self.subrequests.all():
			self.subrequests.remove(user)
			self.save()

class GroupFile(models.Model):
	name = models.CharField(max_length=40)
	group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='files') 
	file = models.FileField(upload_to='groups/group_files', blank=True)

	def __str__(self):
		return self.name