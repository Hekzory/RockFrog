from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.db.models import F
# from django.template import loader
from django.views.generic import View
from communities.models import *
from news_feed.models import *
from notifications import models as notifications
from django.contrib.auth.models import User
# from django.urls import reverse
from .forms import *
import os
from datetime import datetime
import re
import os.path
import json
from itertools import chain
from notifications.models import Notification, Notificationlist


def home(request):
    groups = Group.objects.annotate(members=models.Count('subscribers') + models.Count('editors')).order_by('-members')
    context = {'groups': groups}
    return render(request, 'communities/base.html', context)


def community(request, groupslug):
    if Group.objects.filter(slug=groupslug).exists():
        group = Group.objects.get(slug=groupslug)

        if not group.can_see_group(request.user):
            context = {
                'group': group,
            }
            return render(request, 'communities/closedgroup.html', context)

        personal_in_community_articles = PersonalInCommunityArticle.objects.filter(allowed=True, group=group)
        community_articles = CommunityArticle.objects.filter(allowed=True, group=group)
        articles = sorted(chain(personal_in_community_articles, community_articles),
                          key=lambda instance: instance.pubdate, reverse=True)

        personal_in_community_request_articles = PersonalInCommunityArticle.objects.filter(allowed=False)
        community_request_articles = CommunityArticle.objects.filter(allowed=False)
        request_articles = sorted(chain(personal_in_community_request_articles, community_request_articles),
                                  key=lambda instance: instance.pubdate)

        articles_count = len(articles)
        if request.user.is_authenticated and group.personal_in_community_articles.filter(allowed=False,
                                                                                         author=request.user):
            author_request_articles = group.personal_in_community_articles.filter(allowed=False,
                                                                                  author=request.user).order_by(
                '-pubdate')
        else:
            author_request_articles = []
        context = {
            'group': group,
            'articles': articles,
            'request_articles': request_articles,
            'articles_count': articles_count,
            'author_request_articles': author_request_articles
        }
        return render(request, 'communities/community.html', context)
    else:
        return render(request, 'communities/nogroup.html', status=404)


def information(request, groupslug):
    if Group.objects.filter(slug=groupslug).exists():
        group = Group.objects.get(slug=groupslug)

        if not group.can_see_group(request.user):
            context = {
                'group': group,
            }
            return render(request, 'communities/closedgroup.html', context)

        articles_count = group.community_articles.filter(allowed=True).count()
        context = {'group': group, 'articles_count': articles_count}
        return render(request, 'communities/information.html', context)
    else:
        return render(request, 'communities/nogroup.html')


def collection(request, groupslug):
    if Group.objects.filter(slug=groupslug).exists():
        group = Group.objects.get(slug=groupslug)

        if not group.can_see_group(request.user):
            context = {
                'group': group,
            }
            return render(request, 'communities/closedgroup.html', context)

        articles_count = group.community_articles.filter(allowed=True).count()
        context = {'group': group, 'articles_count': articles_count}
        return render(request, 'communities/collection.html', context)
    else:
        return render(request, 'communities/nogroup.html')


def unsubscribe(request, groupid):
    if request.user.is_authenticated:
        group = Group.objects.get(id=groupid)
        group.unsubscribe(request.user)
    return HttpResponse()


def subscribe(request, groupid):
    if request.user.is_authenticated:
        group = Group.objects.get(id=groupid)
        group.subscribe(request.user)
    return HttpResponse()


def like(request, groupid, articleid):
    if request.user.is_authenticated:
        group = Group.objects.get(id=groupid)
        article = group.articles.get(id=articleid)
        article.like(request.user)
    return HttpResponse()


def removelike(request, groupid, articleid):
    if request.user.is_authenticated:
        group = Group.objects.get(id=groupid)
        article = group.articles.get(id=articleid)
        article.removelike(request.user)
    return HttpResponse()


def createarticle(request, groupid):
    group = Group.objects.get(id=groupid)
    if request.user in group.editors.all() or request.user == group.admin or group.allowarticles == 1 or group.allowarticles == 2:
        if request.POST.get("text", ''):
            if request.POST.get("personal"):
                new_article = PersonalInCommunityArticle(group=group, author=request.user,
                                                         text=request.POST.get("text"))
            else:
                new_article = CommunityArticle(group=group, text=request.POST.get("text"))

            if group.allowarticles == 2 and not (request.user in group.editors.all() or request.user == group.admin):
                new_article.allowed = False
            new_article.save()

            for file in request.FILES.getlist('files'):
                if file.content_type in ['image/png', 'image/jpeg', 'application/pdf', 'text/plain',
                                         'application/msword'] and file.size <= 5000000:
                    new_file = BasicArticleFile(name=file.name, file=file)
                    new_file.save()
                    new_article.files.files.add(new_file)
                    new_article.files.save()

            request.user.profile.last_online_update()
    slug = group.slug
    return HttpResponseRedirect('/groups/' + str(slug) + '/')


class AddToCollection(View):
    def get(self, request, groupid):
        group = Group.objects.get(id=groupid)
        slug = group.slug
        return HttpResponseRedirect('/groups/' + str(slug) + '/collection/')

    def post(self, request, groupid):
        group = Group.objects.get(id=groupid)
        if request.user.is_authenticated and (request.user in group.editors.all() or request.user == group.admin):
            for file in request.FILES.getlist('files'):
                if file.content_type in ['image/png', 'image/jpeg', 'application/pdf', 'text/plain',
                                         'application/msword'] and file.size <= 5000000:
                    new_file = GroupFile(group=group, name=file.name, file=file)
                    new_file.save()

            request.user.profile.last_online_update()
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
            article = BasicArticle.objects.get(id=articleid)
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
                    if file.content_type in ['image/png', 'image/jpeg', 'application/pdf', 'text/plain',
                                             'application/msword'] and file.size <= 5000000:
                        new_file = ArticleFile(article=article, name=file.name, file=file)
                        new_file.save()

            request.user.profile.last_online_update()

        return HttpResponseRedirect('/groups/' + str(slug) + '/')


def creategroup(request):
    if request.user.is_authenticated:
        group = Group(groupname=request.POST.get("groupname"), admin=request.user, pubdate=datetime.now())
        group.save()
        group.slug = str(group.id)
        group.save()

        request.user.profile.last_online_update()
        return HttpResponse(group.slug)
    else:
        return HttpResponse(-1)


def edit(request, groupid):
    group = Group.objects.get(id=groupid)
    if request.user.is_authenticated:
        request.user.profile.last_online_update()
        if request.user in group.editors.all() or request.user == group.admin:
            if request.POST.get('type') == 'allowarticle':
                article = BasicArticle.objects.get(id=request.POST.get('data')).get_child()
                if article.__class__.__name__ != "PersonalArticle" and article.group == group:
                    article.allowed = True
                    article.save()

                    if article.__class__.__name__ == "PersonalInCommunityArticle":
                        if article.author.profile.notificationsettings.post_published_notifications:
                            notifications.create_notification_post_published(group, article.author, 'post_accepted')

                return HttpResponse('Ok')
            elif request.POST.get('type') == 'deletearticle':
                article = BasicArticle.objects.get(id=request.POST.get('data')).get_child()
                if article.__class__.__name__ != "PersonalArticle" and article.group == group:
                    if article.__class__.__name__ == "PersonalInCommunityArticle":
                        if article.author.profile.notificationsettings.post_published_notifications:
                            notifications.create_notification_post_published(group, article.author, 'post_accepted')
                    article.delete()

                return HttpResponse('Ok')
            elif request.POST.get('type') == 'getpost':
                article = BasicArticle.objects.get(id=request.POST.get('data'))
                return HttpResponse(article.text)
            elif request.POST.get('type') == 'deletepost':
                article = BasicArticle.objects.get(id=request.POST.get('data'))

                if request.user != article.author and not article.author is None:
                    try:
                        notification_text = "Ваш пост в " + group.groupname + " удален"
                        notification_name = "Пост удален"
                        notification_href = '/groups/' + group.slug + '/'
                        notification = Notification(not_text=notification_text, not_name=notification_name,
                                                    not_link=notification_href, not_date=datetime.now())
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
            article = BasicArticle.objects.get(id=request.POST.get('data'))
            article.delete()
            return HttpResponse('Ok')
        elif request.POST.get('type') == 'plus' or request.POST.get('type') == 'plusplus':
            basic_article = BasicArticle.objects.get(id=request.POST.get('articleid'))
            if basic_article:
                basic_article.plus(request.user)
        elif request.POST.get('type') == 'remove_plus':
            basic_article = BasicArticle.objects.get(id=request.POST.get('articleid'))
            if basic_article:
                basic_article.remove_plus(request.user)
        elif request.POST.get('type') == 'minus' or request.POST.get('type') == 'minusminus':
            basic_article = BasicArticle.objects.get(id=request.POST.get('articleid'))
            if basic_article:
                basic_article.minus(request.user)
        elif request.POST.get('type') == 'remove_minus':
            basic_article = BasicArticle.objects.get(id=request.POST.get('articleid'))
            if basic_article:
                basic_article.remove_minus(request.user)

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
        request.user.profile.last_online_update()
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
            elif request.POST.get('type') == 'delete':
                group.delete()
                return HttpResponse('deleted')
            elif request.POST.get('type') == 'allowsub':
                user = User.objects.filter(id=request.POST.get('userid'))[0]

                group.subrequests.remove(user)
                group.subscribers.add(user)

                if user.profile.notificationsettings.accepted_to_group_notifications:
                    notifications.create_notification_accepted_to_group(group, user, 'request_accepted')

                return HttpResponse('allowed')
            elif request.POST.get('type') == 'rejectsub':
                user = User.objects.filter(id=request.POST.get('userid'))[0]
                group.subrequests.remove(user)

                if user.profile.notificationsettings.accepted_to_group_notifications:
                    notifications.create_notification_accepted_to_group(group, user, 'request_rejected')

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
                file = request.FILES['groupimage']
                if file.content_type != 'image/png' and file.content_type != 'image/jpeg' and file.size <= 5000000:
                    return HttpResponseRedirect('/groups/' + str(slug) + '/edit/')
                try:
                    os.remove('media/' + group.image.name)
                except:
                    pass
                group.image = request.FILES['groupimage']

                new_article = CommunityArticle(group=group, text='В сообществе обновлена фотография')
                new_article.save()

                new_file = BasicArticleFile(files_list=new_article.files, name=request.FILES['groupimage'].name,
                                            file=request.FILES['groupimage'])
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
                # if user.profile.notificationsettings.accepted_to_group_notifications:
                #	notifications.create_notification_accepted_to_group(group, user, 'banned')
                return HttpResponse(user.username)
            elif request.POST.get('type') == 'cancelban':
                user = User.objects.filter(id=request.POST.get('userid'))[0]
                group.banned.remove(user)
                # if user.profile.notificationsettings.accepted_to_group_notifications:
                #	notifications.create_notification_accepted_to_group(group, user, 'restored')
                return HttpResponse('restored')
            elif request.POST.get('type') == 'toeditor':
                user = User.objects.filter(id=request.POST.get('data'))[0]
                group.subscribers.remove(user)
                group.editors.add(user)
                # if user.profile.notificationsettings.accepted_to_group_notifications:
                #	notifications.create_notification_accepted_to_group(group, user, 'promoted')
                return HttpResponse('Ok')
            elif request.POST.get('type') == 'touser':
                user = User.objects.filter(id=request.POST.get('data'))[0]
                group.editors.remove(user)
                group.subscribers.add(user)
                # if user.profile.notificationsettings.accepted_to_group_notifications:
                #	notifications.create_notification_accepted_to_group(group, user, 'demoted')
                return HttpResponse('Ok')
            elif request.POST.get('type') == 'toadmin':
                user = User.objects.filter(id=request.POST.get('data'))[0]
                group.editors.remove(user)
                group.admin = user
                group.save()
                # if user.profile.notificationsettings.accepted_to_group_notifications:
                #	notifications.create_notification_accepted_to_group(group, user, 'to_admin')
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
            group.send_subrequest(request.user)
            return HttpResponse('sent')
        elif request.POST.get('type') == 'cancelsubrequest':
            group.cancel_subrequest(request.user)
            return HttpResponse('cancelled')
            '''
			if request.user in group.subrequests.all():
				group.subrequests.remove(request.user)
				return HttpResponse('cancelled')
			else:
				group.subrequests.add(request.user)
				return HttpResponse('sent')
			'''
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
