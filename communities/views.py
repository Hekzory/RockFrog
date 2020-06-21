from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.db.models import F
# from django.template import loader
from django.views.generic import View
from communities.models import *
from notifications.models import *
# from .forms import GroupEditForm
from django.contrib.auth.models import User
# from django.urls import reverse
from .forms import *
import os
from datetime import datetime
import re
import os.path

def home(request):
    groups = Group.objects.annotate(members=models.Count('subscribers') + models.Count('editors')).order_by('-members')
    context = {'groups': groups}
    return render(request, 'communities/base.html', context)

def community(request, groupslug):
	if Group.objects.filter(slug=groupslug).exists():
		group = Group.objects.get(slug=groupslug)
		articles = group.articles.filter(allowed=True).order_by('-pubdate')
		articles_count = articles.count()
		requestarticles = group.articles.filter(allowed=False).order_by('-pubdate')
		if group.articles.filter(allowed=False, author=request.user):
			author_request_articles = group.articles.filter(allowed=False, author=request.user).order_by('-pubdate')
		else:
			author_request_articles = []
		context = {
			'group': group,
			'articles': articles,
			'requestarticles': requestarticles,
			'articles_count': articles_count,
			'author_request_articles': author_request_articles
		}
		return render(request, 'communities/community.html', context)
	else:
		return render(request, 'communities/nogroup.html')

def information(request, groupslug):
	if Group.objects.filter(slug=groupslug).exists():
		group = Group.objects.get(slug=groupslug)
		articles_count = group.articles.filter(allowed=True).count()
		context = {'group': group, 'articles_count': articles_count}
		return render(request, 'communities/information.html', context)
	else:
		return render(request, 'communities/nogroup.html')

def collection(request, groupslug):
	if Group.objects.filter(slug=groupslug).exists():
		group = Group.objects.get(slug=groupslug)
		articles_count = group.articles.filter(allowed=True).count()
		context = {'group': group, 'articles_count': articles_count}
		return render(request, 'communities/collection.html', context)
	else:
		return render(request, 'communities/nogroup.html')

def unsubscribe(request, groupid):
	group = Group.objects.get(id=groupid)
	if request.user in group.subscribers.all():
		group.subscribers.remove(request.user)
	elif request.user in group.editors.all():
		group.editors.remove(request.user)
	group.save()
	return HttpResponse()

def subscribe(request, groupid):
	group = Group.objects.get(id=groupid)
	if request.user not in group.subscribers.all() and request.user not in group.editors.all() and request.user not in group.banned.all() and request.user != group.admin:
		group.subscribers.add(request.user)
	group.save()
	return HttpResponse()

def like(request, groupid, articleid):
	group = Group.objects.get(id=groupid)
	article = group.articles.get(id=articleid)
	if request.user not in article.likes.all():
		article.likes.add(request.user)
	article.save()
	return HttpResponse()

def removelike(request, groupid, articleid):
	group = Group.objects.get(id=groupid)
	article = group.articles.get(id=articleid)
	if request.user in article.likes.all():
		article.likes.remove(request.user)
	article.save()
	return HttpResponse()

class CreateArticle(View):
	def get(self, request, groupid):
		group = Group.objects.get(id=groupid)
		slug = group.slug
		return HttpResponseRedirect('/groups/' + str(slug) + '/')

	def post(self, request, groupid):
		group = Group.objects.get(id=groupid)
		if request.user in group.editors.all() or request.user == group.admin or group.allowarticles == 1 or group.allowarticles == 2:
			bound_form = ArticleForm(request.POST)			
			if bound_form.is_valid():
				new_article = bound_form.save(commit=False)
				new_article.group = group
				new_article.author = request.user
				new_article.pubdate = datetime.now()
				if group.allowarticles == 2 and not (request.user in group.editors.all() or request.user == group.admin):	
					new_article.allowed = False
				new_article.save()
				for file in request.FILES.getlist('files'):
					if file.content_type in ['image/png', 'image/jpeg', 'application/pdf', 'text/plain', 'application/msword'] and file.size <= 5000000:					
						new_file = ArticleFile(article=new_article, name=file.name, file=file)
						new_file.save()
		slug = group.slug
		return HttpResponseRedirect('/groups/' + str(slug) + '/')

class AddToCollection(View):
	def get(self, request, groupid):
		group = Group.objects.get(id=groupid)
		slug = group.slug
		return HttpResponseRedirect('/groups/' + str(slug) + '/collection/')

	def post(self, request, groupid):
		group = Group.objects.get(id=groupid)
		for file in request.FILES.getlist('files'):
			if file.content_type in ['image/png', 'image/jpeg', 'application/pdf', 'text/plain', 'application/msword'] and file.size <= 5000000:					
				new_file = GroupFile(group=group, name=file.name, file=file)
				new_file.save()
			
		slug = group.slug
		return HttpResponseRedirect('/groups/' + str(slug) + '/collection/')


class EditArticle(View):
	def get(self, request, groupid, articleid):
		group = Group.objects.get(id=groupid)
		slug = group.slug
		return HttpResponseRedirect('/groups/' + str(slug) + '/')

	def post(self, request, groupid, articleid):
		bound_form = ArticleForm(request.POST)
		group = Group.objects.get(id=groupid)
		slug = group.slug
		if request.user in group.editors.all() or request.user == group.admin:
			article = GroupArticle.objects.get(id=articleid)
			if bound_form.is_valid():
				article.text = request.POST.get("text")
				article.save()

				for fileid in request.POST.get("removedfiles").split():
					try:
						file = article.files.get(id=int(fileid))
						file.delete()
					except:
						pass
				
				for file in request.FILES.getlist('files'):
					if file.content_type in ['image/png', 'image/jpeg', 'application/pdf', 'text/plain', 'application/msword'] and file.size <= 5000000:
						new_file = ArticleFile(article=article, name=file.name, file=file)
						new_file.save()

		return HttpResponseRedirect('/groups/' + str(slug) + '/')

class DeleteArticle(View):
	def get(self, request, groupid, articleid):
		group = Group.objects.get(id=groupid)
		if request.user in group.editors.all() or request.user == group.admin:
			article = GroupArticle.objects.get(id=articleid)

			if request.user != article.author and not article.author is None:
				try:
					notification_text = "Ваш пост в " + group.groupname + " удален"
					notification_name = "Пост удален"
					notification_href = '/groups/' + group.slug + '/'
					notification = Notification(not_text=notification_text, not_name=notification_name, not_link=notification_href, not_date=datetime.now())
					notification.save()
					notificationlist = Notificationlist.objects.get(user=article.author).notifications
					notificationlist.add(notification)
				except:
					print('Notification Error')

			article.delete()
		slug = group.slug
		return HttpResponseRedirect('/groups/' + str(slug) + '/')

	def post(self, request, groupid, articleid):	
		slug = group.slug
		return HttpResponseRedirect('/groups/' + str(slug) + '/')

def creategroup(request):
	if request.user.is_authenticated:
		group = Group(groupname=request.POST.get("groupname"), admin=request.user, pubdate = datetime.now())	
		group.save()
		group.slug = str(group.id)
		group.save()
		return HttpResponse(group.slug)
	else:
		return HttpResponse(-1)

def edit(request, groupid):
	group = Group.objects.get(id=groupid)
	if request.user.is_authenticated:
		if request.user in group.editors.all() or request.user == group.admin:
			if request.POST.get('type') == 'allowarticle':
				article = GroupArticle.objects.get(id=request.POST.get('data'))
				article.allowed = True
				article.pubdate = datetime.now()
				article.save()

				if not article.author is None:
					try:
						notification_text = "Ваш пост в " + group.groupname + " опубликован"
						notification_name = "Пост опубликован"
						notification_href = '/groups/' + group.slug + '/'
						notification = Notification(not_text=notification_text, not_name=notification_name, not_link=notification_href, not_date=datetime.now())
						notification.save()
						notificationlist = Notificationlist.objects.get(user=article.author).notifications
						notificationlist.add(notification)
					except:
						print('Notification Error')

				return HttpResponse('Ok')
			elif request.POST.get('type') == 'deletearticle':
				article = GroupArticle.objects.get(id=request.POST.get('data'))

				if request.user != article.author:
					try:
						notification_text = "Ваш пост в " + group.groupname + " отклонен"
						notification_name = "Пост отклонен"
						notification_href = '/groups/' + group.slug + '/'
						notification = Notification(not_text=notification_text, not_name=notification_name, not_link=notification_href, not_date=datetime.now())
						notification.save()
						notificationlist = Notificationlist.objects.get(user=article.author).notifications
						notificationlist.add(notification)
					except:
						print('Notification Error')

				article.delete()
				return HttpResponse('Ok')
			elif request.POST.get('type') == 'getpost':
				article = GroupArticle.objects.get(id=request.POST.get('data'))
				return HttpResponse(article.text)
			elif request.POST.get('type') == 'deletepost':
				article = GroupArticle.objects.get(id=request.POST.get('data'))

				if request.user != article.author and not article.author is None:
					try:
						notification_text = "Ваш пост в " + group.groupname + " удален"
						notification_name = "Пост удален"
						notification_href = '/groups/' + group.slug + '/'
						notification = Notification(not_text=notification_text, not_name=notification_name, not_link=notification_href, not_date=datetime.now())
						notification.save()
						notificationlist = Notificationlist.objects.get(user=article.author).notifications
						notificationlist.add(notification)
					except:
						print('Notification Error')

				article.delete()
				return HttpResponse('Ok')
			if request.POST.get('type') == 'delete_from_collection':		
				# print(request.POST.get('file'))	
				try:
					groupfile = group.files.get(id=request.POST.get('file'))
					groupfile.delete()
				except:
					pass

				return HttpResponse('Ok')
		if request.POST.get('type') == 'delete_request_article':
			article = GroupArticle.objects.get(id=request.POST.get('data'))
			article.delete()
			return HttpResponse('Ok')
	if request.POST.get('type') == 'delete_from_collection' and not os.path.isfile(request.POST.get('file')):		
		# print(request.POST.get('file'))	
		try:
			groupfile = group.files.get(id=request.POST.get('file'))
			groupfile.delete()
		except:
			pass
		return HttpResponse('Ok')	

	return HttpResponse('error0')

def moreedit(request, groupid):
	if request.user.is_authenticated:
		group = Group.objects.get(id=groupid)
		slug = group.slug
		if request.user in group.editors.all() or request.user == group.admin:
			if request.POST.get('type') == 'public':
				group.public = not group.public
				if group.public:
					for user in group.subrequests.all():
						group.subscribers.add(user)
					group.subrequests.clear()
				group.save()
				return HttpResponse('opened / closed')
			elif request.POST.get('type') == 'delete' and request.user == group.admin:
				group.delete()
				return HttpResponse('deleted')
			elif request.POST.get('type') == 'allowsub':
				user = User.objects.filter(id=request.POST.get('userid'))[0]
				group.subrequests.remove(user)
				group.subscribers.add(user)

				try:
					notification_text = "Вас приняли в сообщество " + group.groupname
					notification_name = "Заявка принята"
					notification_href = '/groups/' + group.slug + '/'
					notification = Notification(not_text=notification_text, not_name=notification_name, not_link=notification_href, not_date=datetime.now())
					notification.save()
					notificationlist = Notificationlist.objects.get(user=user).notifications
					notificationlist.add(notification)
				except:
					pass

				return HttpResponse('allowed')
			elif request.POST.get('type') == 'rejectsub':
				user = User.objects.filter(id=request.POST.get('userid'))[0]
				group.subrequests.remove(user)
				return HttpResponse('rejected')	
			elif request.POST.get('type') == 'allowarticles':				
				group.allowarticles = request.POST.get('data')
				group.save()
				return HttpResponse('Ok')
			elif request.POST.get('type') == 'deletegroupimage':
				try:				
					os.remove('media/' + group.image.name)
				except:
					pass
				group.image = False
				group.save()
				return HttpResponse('Ok')		
			elif request.POST.get('type') == 'uploadimage':
				if request.FILES['groupimage'].content_type != 'image/png' and request.FILES['groupimage'].content_type != 'image/jpeg' and file.size <= 5000000:
					return HttpResponseRedirect('/groups/' + str(slug) + '/edit/')
				try:
					os.remove('media/' + group.image.name)
				except:
					pass
				group.image = request.FILES['groupimage']	

				new_article = GroupArticle(group=group, text='В сообществе обновлена фотография', pubdate=datetime.now())
				new_article.save()
					
				new_file = ArticleFile(article=new_article, name=request.FILES['groupimage'].name, file=request.FILES['groupimage'])
				new_file.save()

				group.save()
				return HttpResponseRedirect('/groups/' + str(slug) + '/edit/')
			elif request.POST.get('type') == 'checkslug':		
				newslug = request.POST.get('slug').lower()

				if newslug.replace(' ', '') == '':
					group.slug = str(group.id)
					group.save()
					return HttpResponse('/groups/' + group.slug + '/edit/')

				if newslug.replace(' ', '') != newslug:
					return HttpResponse('spaces')	

				if newslug == '':
					return HttpResponse('empty')

				pattern = re.compile("^[a-zA-Z]+$") 
				if not pattern.match(newslug):
					return HttpResponse('wrong')

				if newslug == group.slug:
					HttpResponse('/groups/' + group.slug + '/edit/')
				elif newslug == 'create' or Group.objects.filter(slug=newslug).exists():
					return HttpResponse('hasAlready')

				if len(newslug) > 20:
					return HttpResponse('error')

				try:
					group.slug = newslug
					group.save()
				except:
					return HttpResponse('error')

				return HttpResponse('/groups/' + group.slug + '/edit/')
			elif request.POST.get('type') == 'banuser':
				user = User.objects.get(id=request.POST.get('userid'))
				try:
					group.subscribers.remove(user)
				except:
					pass
				try:
					group.editors.remove(user)
				except:
					pass
				group.banned.add(user)
				return HttpResponse(user.username)	
			elif request.POST.get('type') == 'cancelban':
				user = User.objects.filter(id=request.POST.get('userid'))[0]
				group.banned.remove(user)
				return HttpResponse('restored')
			elif request.POST.get('type') == 'toeditor':
				user = User.objects.filter(id=request.POST.get('data'))[0]
				group.subscribers.remove(user)
				group.editors.add(user)
				return HttpResponse('Ok')
			elif request.POST.get('type') == 'touser':
				user = User.objects.filter(id=request.POST.get('data'))[0]
				group.editors.remove(user)
				group.subscribers.add(user)
				return HttpResponse('Ok')
			elif request.POST.get('type') == 'toadmin':
				user = User.objects.filter(id=request.POST.get('data'))[0]
				group.editors.remove(user)
				group.admin = user
				group.save()
				return HttpResponse('Ok')
			elif request.POST.get('type') == 'editname':
				if request.POST.get('data').strip() != '' and len(request.POST.get('data')) <= 48:
					group.groupname = request.POST.get('data')
				group.save()
				return HttpResponse('/groups/' + group.slug + '/edit/')		
			elif request.POST.get('type') == 'editdescription':
				if len(request.POST.get('data')) <= 200:
					group.description = request.POST.get('data')
				group.save()
				return HttpResponse('/groups/' + group.slug + '/edit/')
		elif request.POST.get('type') == 'sendsubrequest':
			if request.user in group.subrequests.all():
				group.subrequests.remove(request.user)
				return HttpResponse('cancelled')
			else:
				group.subrequests.add(request.user)
				return HttpResponse('sent')
	return HttpResponse('error')

def editgroup(request, groupslug):
	if Group.objects.filter(slug=groupslug).exists():
		group = Group.objects.get(slug=groupslug)
		if group.admin != request.user:
			return HttpResponseRedirect('/groups/' + group.slug + '/')
		else:
			group = {'group': group}
			return render(request, 'communities/edit.html', group)
	else:
		return render(request, 'communities/nogroup.html')


'''
class EditGroup(View):
	def get(self, request, groupslug):
		group = Group.objects.filter(slug=groupslug)[0]
		if group.admin != request.user:
			HttpResponseRedirect('../')
		form = GroupEditForm()
		context = {'form': form, 'group': group}
		return render(request, 'communities/edit.html', context)

	def post(self, request, groupslug):	
		# return HttpResponse(request.POST.get('slug'))
		href = '../../' + request.POST.get('slug') + '/edit'
		
		group = Group.objects.filter(slug=groupslug)[0]
		if group.admin != request.user:
			HttpResponseRedirect('../')
		bound_form = GroupEditForm(request.POST)
		form = GroupEditForm()

		if bound_form.is_valid():
			# return HttpResponse(request.POST.get('slug'))	
			group = bound_form.save(group)
			context = {'form': form, 'group': group}
			href = '../../' + request.POST.get('slug') + '/edit'
			# return HttpResponseRedirect(href)
			# return render(request, 'communities/edit.html', context)
		context = {'form': bound_form, 'group': group}
		# return HttpResponse(request.POST.get('slug'))	
		# return render(request, 'communities/edit.html', context)
		return HttpResponseRedirect(href)	
'''