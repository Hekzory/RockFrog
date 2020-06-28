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


class Group(models.Model):
	groupname = models.CharField(max_length=40)
	image = models.ImageField(upload_to='groups/groupimages', default=False)
	slug = models.SlugField(max_length=40, unique=True)
	description = models.TextField(blank=True)
	public = models.BooleanField(default=True)
	allowarticles = models.IntegerField(default=2)
	pubdate = models.DateTimeField('date published', default=datetime.now())
	admin = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='groups_admins')
	editors = models.ManyToManyField(User, blank=True, related_name='groups_editors')
	subscribers = models.ManyToManyField(User, blank=True, related_name='groups_subs')
	subrequests = models.ManyToManyField(User, blank=True, related_name='groups_requests')
	banned = models.ManyToManyField(User, blank=True, related_name='groups_banned')

	def __str__(self):
		return self.groupname

class GroupArticle(models.Model):
	allowed = models.BooleanField(default=True)
	text = models.TextField()	
	pubdate = models.DateTimeField('date published', default=datetime.now())      
	group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='articles') 
	likes = models.ManyToManyField(User, blank=True, related_name='likes')
	author = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='articles_author', default=None)

	def __str__(self):
		return self.text

	def save(self, *args, **kwargs):
	    if self.author is None:
	        self.author = self.group.admin
	    super(GroupArticle, self).save(*args, **kwargs)

class ArticleFile(models.Model):
	name = models.CharField(max_length=40)
	article = models.ForeignKey(GroupArticle, on_delete=models.CASCADE, related_name='files') 
	file = models.FileField(upload_to='groups/articles_files', blank=True)

	def __str__(self):
		return self.name

class GroupFile(models.Model):
	name = models.CharField(max_length=40)
	group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='files') 
	file = models.FileField(upload_to='groups/group_files', blank=True)

	def __str__(self):
		return self.name

class GroupComment(models.Model):
	author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='usercomments')
	parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE, related_name='childrencomments')
	replyto = models.ForeignKey(User, null=True, on_delete=models.PROTECT, related_name='answers')
	article = models.ForeignKey(GroupArticle, on_delete=models.CASCADE, related_name='comments')
	text = models.TextField()
	pubdate = models.DateTimeField('date published', default=datetime.now())

	def __str__(self):
		return self.author.username

'''class GroupList(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	groups = models.ManyToManyField(Group)
	def __str__(self):
		return self.user.username

@receiver(post_save, sender=User)
def create_user_GroupList(sender, instance, created, **kwargs):
	if created:
		GroupList.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_GroupList(sender, instance, **kwargs):
	instance.grouplist.save()	 

class SubscriberList(models.Model):
	group = models.OneToOneField(Group, on_delete=models.CASCADE)
	subscribers = models.ManyToManyField(User)
	def __str__(self):
		return self.group.groupname

@receiver(post_save, sender=Group)
def create_group_SubscriberList(sender, instance, created, **kwargs):
    if created:
        SubscriberList.objects.create(group=instance)

@receiver(post_save, sender=Group)
def save_group_SubscriberList(sender, instance, **kwargs):
    instance.subscriberlist.save()	   

class ArticleList(models.Model):
	group = models.OneToOneField(Group, on_delete=models.CASCADE)
	articles = models.ManyToManyField(Article)
	def __str__(self):
	    return self.group.groupname

@receiver(post_save, sender=Group)
def create_group_ArticleList(sender, instance, created, **kwargs):
    if created:
        ArticleList.objects.create(group=instance)

@receiver(post_save, sender=Group)
def save_group_ArticleList(sender, instance, **kwargs):
    instance.articlelist.save()'''