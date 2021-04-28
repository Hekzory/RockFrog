from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .models import *
from itertools import chain
from django.views.generic import View
from django.db.models import Q
import json
from django.template import loader

global news_feed_url


class ViewArticles(View):
    def get(self, request):
        context = dict()
        context["posts"] = get_hot_posts()
        context['current_app_name'] = "news_feed"
        template = loader.get_template('news_feed/aero/news_feed.html')
        return HttpResponse(template.render(context, request))


def get_hot_posts(user=None):
    news_feed = NewsFeedArticlesList.objects.get(list_type='hot')
    if news_feed.articles.count() == 0:
        news_feed.generate_articles(1000, 50)
    articles = news_feed.articles.select_subclasses().order_by('-rating')
    return articles


def get_subscriptions_posts(user):
    community_articles = CommunityArticle.objects.filter(
        (Q(group__in=user.groups_subs.all()) |
         Q(group__in=user.groups_editors.all()) |
         Q(group__in=user.groups_admins.all())),
        allowed=True)

    personal_in_community_articles = PersonalInCommunityArticle.objects.filter(
        (Q(group__in=user.groups_subs.all()) |
         Q(group__in=user.groups_editors.all()) |
         Q(group__in=user.groups_admins.all())),
        allowed=True)

    articles = sorted(chain(personal_in_community_articles, community_articles), key=lambda instance: instance.pubdate,
                      reverse=True)
    return articles


def get_best_posts(user=None):
    news_feed = NewsFeedArticlesList.objects.get(list_type='best')
    if news_feed.articles.count() == 0:
        news_feed.generate_articles(1000, 50)
    articles = news_feed.articles.select_subclasses().order_by('-rating')
    return articles


def get_reacted_posts(user):
    return BasicArticle.objects.filter(Q(allowed=True) & (Q(pluses__in=[user]) | Q(minuses__in=[user]))).order_by(
        '-pubdate').select_subclasses()


def get_new_posts(user):
    articles = BasicArticle.objects.filter(allowed=True).order_by('-pubdate').select_subclasses()
    articles = [article for article in articles if article.can_see_article(user)]  # bad
    return articles


def get_own_posts(user):
    return BasicArticle.objects.filter(Q(allowed=True) & (Q(author=user))).order_by('-pubdate').select_subclasses()


def generate_self_articles(user):
    return get_own_posts(user)


class GetPosts(View):
    def post(self, request):
        userid = int(request.POST.get('userid'))
        get_posts_functions = {
            "own": get_own_posts,
            "hot": get_hot_posts,
            "best": get_best_posts,
            "new": get_new_posts,
            "reacted": get_reacted_posts,
            "subscriptions": get_subscriptions_posts,
        }
        feed = request.POST.get('feed')
        user = User.objects.get(id=userid) if userid != -1 else None
        posts = get_posts_functions.get(feed, lambda x: None)(user)
        if not posts is None:
            data = json.dumps(serialize_posts(posts, request, title_len=100, text_len=400))
            return JsonResponse(data, safe=False)
        return JsonResponse(None, safe=False)


def serialize_posts(posts, request, title_len=60, text_len=200):
    data = []
    for i in range(len(posts)):
        post = posts[i]
        post_dict = {}
        post_dict["id"] = post.id
        if post.__class__.__name__ == "CommunityArticle":
            post_dict["author"] = post.group.groupname
        elif post.__class__.__name__ == "PersonalInCommunityArticle":
            post_dict["author"] = post.author.username + ' в ' + post.group.groupname
        else:
            post_dict["author"] = post.author.username
        if not post.title:
            post_dict["title"] = "Без названия"
        else:
            if len(post.title) > title_len:
                post_dict["title"] = post.title[:title_len - 1] + '...'
            else:
                post_dict["title"] = post.title
        if len(post.text) > text_len:
            post_dict["text"] = post.text[:text_len - 1] + '...'
        else:
            post_dict["text"] = post.text
        if post.rating > 0:
            post_dict["rating"] = '+' + str(post.rating)
        else:
            post_dict["rating"] = post.rating
        if not request.user.is_authenticated:
            post_dict["react_status"] = "not_user"
        elif request.user in post.pluses.all():
            post_dict["react_status"] = "plus"
        elif request.user in post.minuses.all():
            post_dict["react_status"] = "minus"
        else:
            post_dict["react_status"] = "no_react"
        post_dict["comment_count"] = post.comments.comments.count()
        post_dict["post_link"] = "/article/" + str(post.id)
        post_dict["pubdate"] = datetime.strftime(post.pubdate, '%d.%m.%Y %H:%M')
        if post.__class__.__name__ != "PersonalArticle":
            post_dict["avatar"] = post.group.image.url
        else:
            post_dict["avatar"] = post.author.profile.get_avatar_url()
        data.append(post_dict)
    return data


def generate_subscriptions_articles(user):
    if user.profile.newsfeedsettings.showviewed:
        personal_in_community_articles = PersonalInCommunityArticle.objects.filter((Q(
            group__in=user.groups_subs.all()) | Q(group__in=user.groups_editors.all()) | Q(
            group__in=user.groups_admins.all())), allowed=True)
        community_articles = CommunityArticle.objects.filter(
            Q(group__in=user.groups_subs.all(), allowed=True) | Q(group__in=user.groups_admins.all(), allowed=True))
    else:
        personal_in_community_articles = PersonalInCommunityArticle.objects.filter((Q(
            group__in=user.groups_subs.all()) | Q(group__in=user.groups_editors.all()) | Q(
            group__in=user.groups_admins.all())) & ~Q(views__in=[user]) & Q(allowed=True))
        community_articles = CommunityArticle.objects.filter((Q(group__in=user.groups_subs.all()) | Q(
            group__in=user.groups_admins.all()) | Q(group__in=user.groups_editors.all())) & ~Q(views__in=[user]) & Q(
            allowed=True))

    articles = sorted(chain(personal_in_community_articles, community_articles), key=lambda instance: instance.pubdate,
                      reverse=True)
    return articles


def view_article(request, articleid):
    if BasicArticle.objects.filter(id=articleid).exists():
        article = BasicArticle.objects.get(id=articleid).get_child()
        context = {
            'post': article,
            'title': article.title if article.title else "Пост",
            'current_app_name': 'news_feed',
        }
        # return render(request, 'news_feed/aero/post_page.html', context)
        return render(request, 'news_feed/article.html', context)
    else:
        return render(request, 'news_feed/aero/news_feed_article_404.html')


def manage_settings(request):
    if not request.user.is_authenticated:
        return HttpResponse('Error')
    request.user.profile.last_online_update()

    if request.POST.get('action') == 'set_default_section':
        request.user.profile.newsfeedsettings.defaultsection = request.POST.get('section', 'popular')
        request.user.profile.newsfeedsettings.save()
        return HttpResponse('Ok')

    if request.POST.get('action') == 'switch_show_viewed_settings':
        request.user.profile.newsfeedsettings.showviewed = not request.user.profile.newsfeedsettings.showviewed
        request.user.profile.newsfeedsettings.save()
        return HttpResponse('Ok')


def manage_articles(request):
    if not request.user.is_authenticated:
        return HttpResponse('Error')

    request.user.profile.last_online_update()

    if request.POST.get('action') == 'get_post':
        articleid = request.POST.get('articleid')
        if not BasicArticle.objects.filter(id=articleid).exists():
            return HttpResponse('Error')
        else:
            article = BasicArticle.objects.get(id=articleid).get_child()

        data = {
            'text': article.text,
            'allow_comments': 'true' if article.allow_comments else 'false',
        }
        return HttpResponse(json.dumps(data))

    elif request.POST.get('action') == 'plus_minus':
        if BasicArticle.objects.filter(id=request.POST.get('articleid')):
            article = BasicArticle.objects.get(id=request.POST.get('articleid')).get_child()
            if not article.can_react(request.user):
                return HttpResponse('Error')
        else:
            return HttpResponse('Error')

        if article.can_react(request.user):
            if request.POST.get('type') == 'plus' or request.POST.get('type') == 'plusplus':
                article.plus(request.user)
            elif request.POST.get('type') == 'remove_plus':
                article.remove_plus(request.user)
            elif request.POST.get('type') == 'minus' or request.POST.get('type') == 'minusminus':
                article.minus(request.user)
            elif request.POST.get('type') == 'remove_minus':
                article.remove_minus(request.user)

        return HttpResponse('Ok')

    elif request.POST.get('action') == 'mark_viewed':
        articleid = request.POST.get('articleid')
        if not BasicArticle.objects.filter(id=articleid).exists():
            return HttpResponse('Error')
        else:
            article = BasicArticle.objects.get(id=articleid).get_child()

        if article.can_see_article(request.user):
            value = request.POST.get('value')
            value = True if value == 'true' else False

            if value and request.user not in article.views.all():
                article.views.add(request.user)
                article.save()
            elif (not value) and request.user in article.views.all():
                article.views.remove(request.user)
                article.save()
            return HttpResponse('Ok')
        return HttpResponse('Error')

    elif request.POST.get('action') == 'create_personal_article':
        allow_comments = True if request.POST.get('allow_comments') == 'on' else False

        if request.POST.get("text", ''):
            new_article = PersonalArticle(author=request.user, text=request.POST.get("text"),
                                          allow_comments=allow_comments)
            new_article.save()

            for file in request.FILES.getlist('files'):
                if file.content_type in ['image/png', 'image/jpeg', 'application/pdf', 'text/plain',
                                         'application/msword'] and file.size <= 5000000:
                    new_file = BasicArticleFile(name=file.name.replace("'", "").replace('"', ''), file=file,
                                                files_list=new_article.files)
                    new_file.save()

        return HttpResponseRedirect(request.POST.get('return_url', news_feed_url))

    elif request.POST.get('action') == 'create_community_article':
        personal = True if request.POST.get('personal') == 'on' else False
        allow_comments = True if request.POST.get('allow_comments') == 'on' else False

        groupid = request.POST.get('groupid')
        group = Group.objects.get(id=groupid)

        if request.user in group.editors.all() or request.user == group.admin or group.allowarticles == 1 or group.allowarticles == 2:
            if request.POST.get("text", ''):
                if personal:
                    new_article = PersonalInCommunityArticle(group=group, author=request.user,
                                                             text=request.POST.get("text"),
                                                             allow_comments=allow_comments)
                else:
                    new_article = CommunityArticle(group=group, text=request.POST.get("text"),
                                                   allow_comments=allow_comments)

                if group.allowarticles == 2 and not (
                        request.user in group.editors.all() or request.user == group.admin):
                    new_article.allowed = False
                new_article.save()

                for file in request.FILES.getlist('files'):
                    if file.content_type in ['image/png', 'image/jpeg', 'application/pdf', 'text/plain',
                                             'application/msword'] and file.size <= 5000000:
                        new_file = BasicArticleFile(name=file.name.replace("'", "").replace('"', ''), file=file,
                                                    files_list=new_article.files)
                        new_file.save()

        slug = group.slug
        return HttpResponseRedirect('/groups/' + str(slug) + '/')

    elif request.POST.get('action') == 'edit_article':
        articleid = request.POST.get('articleid')

        if not BasicArticle.objects.filter(id=articleid).exists():
            return HttpResponseRedirect(request.POST.get('return_url'))
        else:
            article = BasicArticle.objects.get_subclass(id=articleid)

        if not article.can_edit_article(request.user):
            return HttpResponseRedirect(request.POST.get('return_url'))

        if not request.POST.get("text", ''):
            return HttpResponseRedirect(request.POST.get('return_url'))

        allow_comments = True if request.POST.get('allow_comments') == 'on' else False
        article.allow_comments = allow_comments
        article.text = request.POST.get("text")
        article.save()
        for fileid in request.POST.get("removedfiles").split():
            try:
                file = article.files.get(id=int(fileid))
                file.delete()
            except Exception as ex:
                pass

        for file in request.FILES.getlist('files'):
            if file.content_type in ['image/png', 'image/jpeg', 'application/pdf', 'text/plain',
                                     'application/msword'] and file.size <= 5000000:
                new_file = BasicArticleFile(files_list=article.files, name=file.name.replace("'", "").replace('"', ''),
                                            file=file)
                new_file.save()

        return HttpResponseRedirect(request.POST.get('return_url'))

    elif request.POST.get('action') == 'delete_article':
        articleid = request.POST.get('articleid')
        article = BasicArticle.objects.get_subclass(id=articleid)

        if article.has_rights(request.user):
            article.delete()

        return HttpResponse('Ok')


def manage_comments(request):
    if not request.user.is_authenticated:
        return HttpResponse('Error')

    if request.POST.get('action') == 'plus_minus':
        if BasicComment.objects.filter(id=request.POST.get('commentid')):
            comment = BasicComment.objects.get(id=request.POST.get('commentid'))
            if not comment.comments_list.article.get_child().can_comment_article(
                    request.user) or not comment.comments_list.article.get_child().can_see_article(request.user):
                return HttpResponse('Error')
        else:
            return HttpResponse('Error')

        if request.POST.get('type') == 'plus' or request.POST.get('type') == 'plusplus':
            comment.plus(request.user)
        elif request.POST.get('type') == 'remove_plus':
            comment.remove_plus(request.user)
        elif request.POST.get('type') == 'minus' or request.POST.get('type') == 'minusminus':
            comment.minus(request.user)
        elif request.POST.get('type') == 'remove_minus':
            comment.remove_minus(request.user)

        return HttpResponse('Ok')

    elif request.POST.get('action') == 'create_comment':

        articleid = request.POST.get('articleid')
        if not BasicArticle.objects.filter(id=articleid).exists():
            return HttpResponse('Error')
        else:
            article = BasicArticle.objects.get(id=articleid).get_child()

        if not article.allow_comments:
            return HttpResponse('Error')

        if article.__class__.__name__ != 'PersonalArticle':
            group = article.group
            if not group.can_see_group(request.user):
                return HttpResponse('Error')

        comment_text = request.POST.get('text')
        if comment_text.replace(' ', '').rstrip() == '':
            return HttpResponse('empty')
        if len(comment_text) > 750:
            return HttpResponse('long')

        new_comment = BasicComment(author=request.user, text=comment_text, comments_list=article.comments)
        new_comment.save()

        data = {
            'avatar': '/media/' + str(request.user.profile.avatar),
            'text': comment_text,
            'author': request.user.username,
            'pubdate': str(new_comment.pubdate),
            'postid': article.id,
            'commentid': new_comment.id,
            'locationid': 'post' + str(articleid) + 'comments',
            'parentname': ''
        }

        replycommentid = request.POST.get('reply')
        if replycommentid != '' and BasicComment.objects.filter(id=int(replycommentid)).exists():
            replycomment = BasicComment.objects.get(id=int(replycommentid))
            replyuser = replycomment.author
            new_comment.replyto = replyuser
            if not replycomment.parent:
                new_comment.parent = replycomment
                new_comment.save()
            else:
                new_comment.parent = replycomment.parent
                new_comment.save()

            data['locationid'] = 'comment' + str(new_comment.parent.id) + 'children'
            data['parentname'] = replyuser.username

        request.user.profile.last_online_update()
        return HttpResponse(json.dumps(data))

    elif request.POST.get('action') == 'delete_comment':

        commentid = request.POST.get('commentid')
        if not BasicComment.objects.filter(id=commentid).exists():
            return HttpResponse('Error')
        else:
            comment = BasicComment.objects.get(id=commentid)

        article = comment.comments_list.article.get_child()

        if not article.allow_comments:
            return HttpResponse('Error')

        if article.__class__.__name__ != 'PersonalArticle':
            group = article.group
            if not group.can_see_group(request.user):
                return HttpResponse('Error')

        if request.user == comment.author:
            if comment.childrencomments.all():
                comment.is_deleted = True
                comment.save()
                return HttpResponse('is_deleted')
            else:
                if comment.parent and comment.parent.is_deleted and comment.parent.childrencomments.count() == 1:
                    comment.parent.delete()
                else:
                    comment.delete()
            request.user.profile.last_online_update()
            return HttpResponse('Ok')
        return HttpResponse('Error')

    elif request.POST.get('action') == 'edit_comment':
        commentid = request.POST.get('commentid')
        if not BasicComment.objects.filter(id=commentid).exists():
            return HttpResponse('Error')
        else:
            comment = BasicComment.objects.get(id=commentid)

        article = comment.comments_list.article.get_child()

        if not article.allow_comments:
            return HttpResponse('Error')

        if article.__class__.__name__ != 'PersonalArticle':
            group = article.group
            if not group.can_see_group(request.user):
                return HttpResponse('Error')

        if request.user == comment.author:
            commenttext = request.POST.get('text')
            if commenttext.replace(' ', '').rstrip() == '':
                return HttpResponse('empty')
            if len(commenttext) > 750:
                return HttpResponse('long')
            comment.text = commenttext
            comment.save()

            request.user.profile.last_online_update()
            return HttpResponse('Ok')
        return HttpResponse('Error')
    return HttpResponse('Ok')
