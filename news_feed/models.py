import datetime
from datetime import timedelta
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from communities.models import *
from django.db.models import Q
import os
from django.db.models.signals import post_delete
from model_utils.managers import InheritanceManager


def get_total_hours(date):
	return int(date.timestamp()) // (3600)

class CommentsList(models.Model):
	pass

class ArticleFilesList(models.Model):

	def images(self):
		images = [file.id for file in self.files.all() if file.extension() in ['png', 'jpg']]
		images = self.files.filter(id__in=images)
		return images

	def not_images(self):
		images = [file.id for file in self.files.all() if file.extension() not in ['png', 'jpg']]
		images = self.files.filter(id__in=images)
		return images

class BasicArticleFile(models.Model):
	name = models.CharField(max_length=40)
	file = models.FileField(upload_to='groups/articles_files', blank=True)
	files_list = models.ForeignKey(ArticleFilesList, on_delete=models.CASCADE, null=True, related_name='files')

	def __str__(self):
		return self.name

	def extension(self):
		name, extension = os.path.splitext(self.file.name)
		return extension[1:]

class BasicComment(models.Model):
	author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='comments')
	parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.PROTECT, related_name='childrencomments')
	replyto = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT, related_name='%(class)s_answers_made')
	text = models.TextField()
	is_deleted = models.BooleanField(default=False)
	pubdate = models.DateTimeField('date published', default=datetime.now)
	pluses = models.ManyToManyField(User, blank=True, related_name='%(class)s_pluses_made')
	minuses = models.ManyToManyField(User, blank=True, related_name='%(class)s_minuses_made')
	comments_list = models.ForeignKey(CommentsList, on_delete=models.CASCADE, null=True, related_name='comments')

	rating = models.FloatField(null=True, blank=True, default=0)

	def can_plus(self, user):
		return self.comments_list.article.get_child().can_comment_article(user) and self.author != user

	def update_rating(self):
		self.rating = self.pluses.count() - self.minuses.count()
		self.save()

	def increase_rating(self):
		self.rating += 1
		self.author.profile.rating += 0.5
		self.author.profile.save()
		self.save()

	def decrease_rating(self):
		self.rating -= 1
		self.author.profile.rating -= 0.5
		self.author.profile.save()
		self.save()

	def plus(self, user):
		if user not in self.pluses.all():
			self.pluses.add(user)
			self.increase_rating()
		if user in self.minuses.all():
			self.minuses.remove(user)	
			self.increase_rating()	
		self.save()

	def minus(self, user):
		if user in self.pluses.all():
			self.pluses.remove(user)
			self.decrease_rating()
		if user not in self.minuses.all():
			self.minuses.add(user)
			self.decrease_rating()
		self.save()

	def remove_plus(self, user):
		if user in self.pluses.all():
			self.pluses.remove(user)
			self.decrease_rating()
			self.save()

	def remove_minus(self, user):
		if user in self.minuses.all():
			self.minuses.remove(user)
			self.increase_rating()
			self.save()

	def __str__(self):
		return self.text

class BasicArticle(models.Model):
	allowed = models.BooleanField(default=True)
	author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='articles', null=True, blank=True)
	title = models.TextField(max_length=40, null=True, blank=True)
	text = models.TextField()	
	pubdate = models.DateTimeField('date published', default=datetime.now)      
	pluses = models.ManyToManyField(User, blank=True, related_name='plused_articles')
	minuses = models.ManyToManyField(User, blank=True, related_name='minused_articles')
	views = models.ManyToManyField(User, blank=True, related_name='viewed_articles')
	allow_comments = models.BooleanField(default=True, null=True)
	comments = models.OneToOneField(CommentsList, on_delete=models.CASCADE, null=True, blank=True, related_name="article")
	files = models.OneToOneField(ArticleFilesList, on_delete=models.CASCADE, null=True, blank=True, related_name="article")

	rating = models.FloatField(null=True, blank=True, default=0)

	objects = InheritanceManager()

	def class_name(self):
		return self.__class__.__name__

	def has_rights(self, user):
		return False

	def can_plus_or_comment(self, user):
		return False

	def can_plus_article(self, user):
		if self.__class__.__name__ != 'CommunityArticle':
			return user.is_authenticated and self.can_see_article(user) and self.author != user
		return user.is_authenticated and self.can_see_article(user)

	def update_rating(self):
		article = self.get_child()
		article.rating = article.pluses.count() - article.minuses.count()
		article.save()

	def increase_rating(self):		
		article = self.get_child()
		article.rating += 1
		if article.__class__.__name__ == 'PersonalArticle':
			article.author.profile.rating += 1
			article.author.profile.save()			
		elif article.__class__.__name__ == 'PersonalInCommunityArticle':
			article.author.profile.rating += 1
			article.group.rating += 1
			article.author.profile.save()
			article.group.save()
		elif article.__class__.__name__ == 'CommunityArticle':
			article.group.rating += 1
			article.group.save()
		article.save()

	def decrease_rating(self):		
		article = self.get_child()
		article.rating -= 1
		if article.__class__.__name__ == 'PersonalArticle':
			article.author.profile.rating -= 1
			article.author.profile.save()
		elif article.__class__.__name__ == 'PersonalInCommunityArticle':
			article.author.profile.rating -= 1
			article.group.rating -= 1
			article.author.profile.save()
			article.group.save()
		elif article.__class__.__name__ == 'CommunityArticle':
			article.group.rating -= 1
			article.group.save()
		article.save()

	def can_see_article(self, user):
		return False

	def can_edit_article(self, user):
		if self.__class__.__name__ != 'PersonalArticle':
			return self.group.has_power(user) or (not self.allowed and self.__class__.__name__ == 'PersonalInCommunityArticle' and self.author == user)
		return user == self.author

	def can_comment_article(self, user):
		return self.allow_comments and self.can_see_article(user)

	def get_child(self):
		return BasicArticle.objects.get_subclass(id=self.id)

	def get_child_type(self):
		return BasicArticle.objects.get_subclass(id=self.id).class_name()

	def plus(self, user):
		if user not in self.pluses.all():
			self.pluses.add(user)
			self.increase_rating()
		if user in self.minuses.all():
			self.minuses.remove(user)
			self.increase_rating()		
		self.save()

	def minus(self, user):
		if user in self.pluses.all():
			self.pluses.remove(user)
			self.decrease_rating()
		if user not in self.minuses.all():
			self.minuses.add(user)
			self.decrease_rating()
		self.save()

	def remove_plus(self, user):
		if user in self.pluses.all():
			self.pluses.remove(user)
			self.decrease_rating()
			self.save()

	def remove_minus(self, user):
		if user in self.minuses.all():
			self.minuses.remove(user)
			self.increase_rating()
			self.save()

	def get_rating(self):
		return self.pluses.count()-self.minuses.count()

	def __str__(self):
		if self.title:
			return self.title
		return self.text

class PersonalArticle(BasicArticle):
	
	def can_see_article(self, user):
		return True

	def has_rights(self, user):
		return self.allowed and self.author == user

	def can_plus_or_comment(self, user):
		return self.allowed and user not in self.author.profile.blacklist.all()

class CommunityArticle(BasicArticle):
	group = models.ForeignKey(Group, on_delete=models.PROTECT, related_name='community_articles')

	def can_see_article(self, user):
		return self.group.public	

	def has_rights(self, user):
		return self.group.has_power(user)

	def can_plus_or_comment(self, user):
		return self.allowed and self.group.can_see_group(user)

class PersonalInCommunityArticle(BasicArticle):
	group = models.ForeignKey(Group, on_delete=models.PROTECT, related_name='personal_in_community_articles')

	def can_see_article(self, user):
		return self.group.public	

	def has_rights(self, user):
		return self.group.has_power(user)	

	def can_plus_or_comment(self, user):
		return self.allowed and self.group.can_see_group(user)

class NewsFeedArticlesList(models.Model):
	articles = models.ManyToManyField(BasicArticle, blank=True, null=True)
	list_type = models.CharField(max_length=40, default='best')

	def generate_articles(self, days, limit):	
		minimum_date = datetime.now() - timedelta(days=days)
		articles = BasicArticle.objects.filter(allowed=True, pubdate__gte=minimum_date)[:limit] 
		self.articles.set(articles)

	def __str__(self):
		return self.list_type

@receiver(post_save, sender=PersonalArticle)
@receiver(post_save, sender=CommunityArticle)
@receiver(post_save, sender=PersonalInCommunityArticle)
def create_comments_and_files(sender, instance, created, **kwargs):
    if created:
    	new_comments_list = CommentsList()
    	new_comments_list.save()
    	new_files_list = ArticleFilesList()
    	new_files_list.save()
    	instance.comments = new_comments_list
    	instance.files = new_files_list
    	instance.save()

@receiver(post_delete, sender=BasicArticle)
def post_delete_user(sender, instance, *args, **kwargs):
    if instance.comments:
        instance.comments.delete()
    if instance.files:
        instance.files.delete()