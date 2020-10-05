from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from django.template import loader
from django.contrib.auth.models import User
from django.views.generic import View
from .forms import *
from news_feed.models import *
from news_feed.views import generate_self_articles
# Create your views here.


class UserProfileView(View):
    def get(self, request, username):
        template = None
        if User.objects.filter(username=username).first() is not None:
            viewed_user = User.objects.get(username=username)
            context = {'user': viewed_user}
        else:
            context = dict()
            template = loader.get_template('UserProfile/user_not_found.html')
            return HttpResponse(template.render(context, request), status=404)
        if request.user.is_authenticated:
            if request.user.id == viewed_user.id:
                return HttpResponseRedirect('/profile')
            blacklist = request.user.profile.blacklist
            viewed_user_blacklist = viewed_user.profile.blacklist
            if blacklist.filter(pk=viewed_user.pk).exists():
                in_list = True
            else:
                in_list = False
            context['in_list'] = in_list

            if viewed_user_blacklist.filter(pk=request.user.pk).exists():
                template = loader.get_template('UserProfile/blocked_forbidden.html')
            else:
                template = loader.get_template('UserProfile/userprofile.html')
        else:
            if viewed_user.profile.privacysettings.allow_to_view_for_unreg:
                template = loader.get_template('UserProfile/userprofile.html')
            else:
                template = loader.get_template('UserProfile/unregistered_forbidden.html')
        return HttpResponse(template.render(context, request))


class YourProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/")
        else:
            template = loader.get_template('UserProfile/aero/own_profile_main.html')
            context = dict()
            context['current_app_name'] = "profile"
            context['posts'] = generate_self_articles(request.user)
            return HttpResponse(template.render(context, request))

    # Устаревшая версия, функционирующая со старым дизайном
    def get_deprecated(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/")
        else:
            template = loader.get_template('UserProfile/yourprofile.html')
            context = dict()
            return HttpResponse(template.render(context, request))


class EditProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/')
        else:
            initial_params = dict()
            initial_params['about'] = request.user.profile.about
            initial_params['birth_date'] = request.user.profile.birth_date
            initial_params['email'] = request.user.profile.email
            initial_params['city'] = request.user.profile.city
            initial_params['phone'] = request.user.profile.phone
            initial_params['interests'] = request.user.profile.interests
            form = ProfileForm(initial=initial_params)
            context = {'form': form}
            context['current_app_name'] = "profile"
            template = loader.get_template('UserProfile/editprofile.html')
            return HttpResponse(template.render(context, request))

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/")
        else:
            request.user.profile.last_online_update()
            bound_form = ProfileForm(request.POST, request.FILES)
            check = bound_form.is_valid()
            if check:
                bound_form.change_profile(request.user, request.FILES)
                initial_params = dict()
                initial_params['about'] = request.user.profile.about
                initial_params['birth_date'] = request.user.profile.birth_date
                initial_params['email'] = request.user.profile.email
                initial_params['city'] = request.user.profile.city
                initial_params['phone'] = request.user.profile.phone
                initial_params['interests'] = request.user.profile.interests
                template = loader.get_template('UserProfile/editprofile.html')
                form = ProfileForm(initial=initial_params)
                context = {'form': form}
                context['current_app_name'] = "profile"
                return HttpResponse(template.render(context, request))
            else:
                template = loader.get_template('UserProfile/editprofile.html')
                context = {'form': bound_form}
                return HttpResponse(template.render(context, request))


class EditPrivacyView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/')
        else:
            initial_params = dict()
            initial_params['allow_to_view_for_unreg'] = request.user.profile.privacysettings.allow_to_view_for_unreg
            template = loader.get_template('UserProfile/aero/edit_privacy.html')
            form = PrivacySettingsForm(initial=initial_params)
            context = {'form': form}
            context['current_app_name'] = "profile"
            return HttpResponse(template.render(context, request))

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/')
        else:
            request.user.profile.last_online_update()
            bound_form = PrivacySettingsForm(request.POST)
            check = bound_form.is_valid()
            if check:
                bound_form.change_privacy_settings(request.user)
                initial_params = dict()
                initial_params['allow_to_view_for_unreg'] = request.user.profile.privacysettings.allow_to_view_for_unreg
                template = loader.get_template('UserProfile/aero/edit_privacy.html')
                form = PrivacySettingsForm(initial=initial_params)
                context = {'form': form}
                context['current_app_name'] = "profile"
                return HttpResponse(template.render(context, request))
            else:
                template = loader.get_template('UserProfile/aero/edit_privacy.html')
                context = {'form': bound_form}
                context['current_app_name'] = "profile"
                return HttpResponse(template.render(context, request))

    def get_deprecated(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/')
        else:
            initial_params = dict()
            initial_params['allow_to_view_for_unreg'] = request.user.profile.privacysettings.allow_to_view_for_unreg
            template = loader.get_template('UserProfile/edit_privacy.html')
            form = PrivacySettingsForm(initial=initial_params)
            context = {'form': form}
            context['current_app_name'] = "profile"
            return HttpResponse(template.render(context, request))

    def post_deprecated(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/')
        else:
            request.user.profile.last_online_update()
            bound_form = PrivacySettingsForm(request.POST)
            check = bound_form.is_valid()
            if check:
                bound_form.change_privacy_settings(request.user)
                initial_params = dict()
                initial_params['allow_to_view_for_unreg'] = request.user.profile.privacysettings.allow_to_view_for_unreg
                template = loader.get_template('UserProfile/edit_privacy.html')
                form = PrivacySettingsForm(initial=initial_params)
                context = {'form': form}
                context['current_app_name'] = "profile"
                return HttpResponse(template.render(context, request))
            else:
                template = loader.get_template('UserProfile/edit_privacy.html')
                context = {'form': bound_form}
                context['current_app_name'] = "profile"
                return HttpResponse(template.render(context, request))


class EditNotificationsView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/')
        else:
            context = dict()
            context['user'] = request.user
            context['personal_message_notifications'] = request.user.profile.notificationsettings.personal_message_notifications
            context['accepted_to_group_notifications'] = request.user.profile.notificationsettings.accepted_to_group_notifications
            context['post_published_notifications'] = request.user.profile.notificationsettings.post_published_notifications
            context['current_app_name'] = "profile"
            template = loader.get_template('UserProfile/aero/edit_notifications.html')
            return HttpResponse(template.render(context, request))

    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'NotAuthenticated'})
        type = request.POST['type']
        current_state = request.POST['current_state'] == 'true'
        if type == 'personal_message_notifications':
            request.user.profile.notificationsettings.personal_message_notifications = current_state
            request.user.profile.notificationsettings.save()
            return JsonResponse({'status': 'ok'})
        elif type == 'accepted_to_group_notifications':
            request.user.profile.notificationsettings.accepted_to_group_notifications = current_state
            request.user.profile.notificationsettings.save()
            return JsonResponse({'status': 'ok'})
        elif type == 'post_published_notifications':
            request.user.profile.notificationsettings.post_published_notifications = current_state
            request.user.profile.notificationsettings.save()
            return JsonResponse({'status': 'ok'})

    def get_deprecated(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/')
        else:
            context = dict()
            context['user'] = request.user
            context['personal_message_notifications'] = request.user.profile.notificationsettings.personal_message_notifications
            context['accepted_to_group_notifications'] = request.user.profile.notificationsettings.accepted_to_group_notifications
            context['post_published_notifications'] = request.user.profile.notificationsettings.post_published_notifications
            context['current_app_name'] = "profile"
            template = loader.get_template('UserProfile/edit_notifications.html')
            return HttpResponse(template.render(context, request))

    def post_deprecated(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'NotAuthenticated'})
        type = request.POST['type']
        current_state = request.POST['current_state'] == 'true'
        if type == 'personal_message_notifications':
            request.user.profile.notificationsettings.personal_message_notifications = current_state
            request.user.profile.notificationsettings.save()
            return JsonResponse({'status': 'ok'})
        elif type == 'accepted_to_group_notifications':
            request.user.profile.notificationsettings.accepted_to_group_notifications = current_state
            request.user.profile.notificationsettings.save()
            return JsonResponse({'status': 'ok'})
        elif type == 'post_published_notifications':
            request.user.profile.notificationsettings.post_published_notifications = current_state
            request.user.profile.notificationsettings.save()
            return JsonResponse({'status': 'ok'})


class EditSecurityView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/')
        else:
            template = loader.get_template('UserProfile/aero/edit_security.html')
            form = ChangePasswordForm()
            context = {'form': form}
            context['current_app_name'] = "profile"
            return HttpResponse(template.render(context, request))

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/')
        else:
            request.user.profile.last_online_update()
            bound_form = ChangePasswordForm(request.POST)
            check = bound_form.is_valid()
            if check:
                result = bound_form.change_password(request.user)
                new_form = ChangePasswordForm()
                context = {'change_error': not result, 'form' : new_form}
                context['current_app_name'] = "profile"
                if context['change_error']:
                    template = loader.get_template('UserProfile/aero/edit_security.html')
                else:
                    template = loader.get_template('UserProfile/aero/password_changed.html')
                return HttpResponse(template.render(context, request))
            else:
                template = loader.get_template('UserProfile/aero/edit_security.html')
                context = {'form': bound_form}
                context['current_app_name'] = "profile"
                return HttpResponse(template.render(context, request))

    def get_deprecated(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/')
        else:
            template = loader.get_template('UserProfile/edit_security.html')
            form = ChangePasswordForm()
            context = {'form': form}
            context['current_app_name'] = "profile"
            return HttpResponse(template.render(context, request))

    def post_deprecated(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/')
        else:
            request.user.profile.last_online_update()
            bound_form = ChangePasswordForm(request.POST)
            check = bound_form.is_valid()
            if check:
                result = bound_form.change_password(request.user)
                new_form = ChangePasswordForm()
                context = {'change_error': not result, 'form' : new_form}
                context['current_app_name'] = "profile"
                if context['change_error']:
                    template = loader.get_template('UserProfile/edit_security.html')
                else:
                    template = loader.get_template('UserProfile/password_changed.html')
                return HttpResponse(template.render(context, request))
            else:
                template = loader.get_template('UserProfile/edit_security.html')
                context = {'form': bound_form}
                context['current_app_name'] = "profile"
                return HttpResponse(template.render(context, request))


class BlockedUsersView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/')
        else:
            template = loader.get_template('UserProfile/aero/blacklist.html')
            context = {'blacklist': request.user.profile.blacklist.all()}
            context['current_app_name'] = "profile"
            return HttpResponse(template.render(context, request))

    def get_deprecated(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/')
        else:
            template = loader.get_template('UserProfile/blacklist.html')
            context = {'blacklist': request.user.profile.blacklist.all()}
            context['current_app_name'] = "profile"
            return HttpResponse(template.render(context, request))


class BlockUserView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'NotAuthenticated'})
        else:
            try:
                user_id = int(request.POST['user_id'])
            except ValueError:
                return JsonResponse({'status': 'User_id is not a number'})
            if user_id == request.user.id:
                return JsonResponse({'status': 'CantBlockYourself'})
            if User.objects.filter(id=user_id).first() is None:
                return JsonResponse({'status': 'UserNotFound'})
            blacklist = request.user.profile.blacklist
            blocked_user = User.objects.get(id=user_id)
            if not blacklist.filter(pk=blocked_user.pk).exists():
                blacklist.add(blocked_user)
            return JsonResponse({'status': 'ok'})


class UnblockUserView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'NotAuthenticated'})
        else:
            try:
                user_id = int(request.POST['user_id'])
            except ValueError:
                return JsonResponse({'status': 'User_id is not a number'})
            if User.objects.filter(id=user_id).first() is None:
                return JsonResponse({'status': 'UserNotFound'})
            blacklist = request.user.profile.blacklist
            blocked_user = User.objects.get(id=user_id)
            if blacklist.filter(pk=blocked_user.pk).exists():
                blacklist.remove(blocked_user)
            return JsonResponse({'status': 'ok'})


class ProfileSettings(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/")
        else:
            template = loader.get_template('UserProfile/aero/profile_settings.html')
            context = dict()
            context['current_app_name'] = "profile"
            context['user'] = request.user
            return HttpResponse(template.render(context, request))


def update_rating_lite(request):
    user = request.user
    user.profile.rating = 0

    for article in user.personal_articles.all():
        user.profile.rating += article.rating

    for article in user.personal_in_community_articles.all():
        user.profile.rating += article.rating

    for comment in user.comments.all():
        user.profile.rating += comment.rating / 2

    user.profile.save()
    return HttpResponseRedirect('/profile/')


def update_rating(request):
    user = request.user
    user.profile.rating = 0

    for article in user.articles.select_subclasses(PersonalArticle, PersonalInCommunityArticle).all():
        article.update_rating()
        user.profile.rating += article.rating

    for comment in user.comments.all():
        comment.update_rating()
        user.profile.rating += comment.rating / 2

    user.profile.save()
    return HttpResponseRedirect('/profile/')


