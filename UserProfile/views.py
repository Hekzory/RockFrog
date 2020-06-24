from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.template import loader
from django.contrib.auth.models import User
from django.views.generic import View
from .forms import *
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
            template = loader.get_template('UserProfile/yourprofile.html')
            form = ProfileForm()
            context = {'form' : form}
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
            template = loader.get_template('UserProfile/editprofile.html')
            return HttpResponse(template.render(context, request))

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/")
        else:
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
            template = loader.get_template('UserProfile/edit_privacy.html')
            form = PrivacySettingsForm(initial=initial_params)
            context = {'form': form}
            return HttpResponse(template.render(context, request))

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/')
        else:
            bound_form = PrivacySettingsForm(request.POST)
            check = bound_form.is_valid()
            if check:
                bound_form.change_privacy_settings(request.user)
                initial_params = dict()
                initial_params['allow_to_view_for_unreg'] = request.user.profile.privacysettings.allow_to_view_for_unreg
                template = loader.get_template('UserProfile/edit_privacy.html')
                form = PrivacySettingsForm(initial=initial_params)
                context = {'form': form}
                return HttpResponse(template.render(context, request))
            else:
                template = loader.get_template('UserProfile/edit_privacy.html')
                context = {'form': bound_form}
                return HttpResponse(template.render(context, request))


class EditSecurityView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/')
        else:
            template = loader.get_template('UserProfile/edit_security.html')
            form = ChangePasswordForm()
            context = {'form': form}
            return HttpResponse(template.render(context, request))

    def post(self, request):
        bound_form = ChangePasswordForm(request.POST)
        check = bound_form.is_valid()
        if check:
            result = bound_form.change_password(request.user)
            new_form = ChangePasswordForm()
            context = {'change_error': not result, 'form' : new_form}
            template = loader.get_template('UserProfile/password_changed.html')
            return HttpResponse(template.render(context, request))
        else:
            template = loader.get_template('UserProfile/edit_security.html')
            context = {'form': bound_form}
            return HttpResponse(template.render(context, request))


class BlockedUsersView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/')
        else:
            template = loader.get_template('UserProfile/blacklist.html')
            context = {'blacklist': request.user.profile.blacklist.all()}
            return HttpResponse(template.render(context, request))


class BlockUserView(View):
    def get(self, request, username):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/')
        else:
            if username == request.user.username:
                return HttpResponseRedirect('/profile')
            if User.objects.filter(username=username).first() is None:
                template = loader.get_template('UserProfile/user_not_found.html')
                return HttpResponse(template.render(dict(), request), status=404)
            blacklist = request.user.profile.blacklist
            blocked_user = User.objects.get(username=username)

            if not blacklist.filter(pk=blocked_user.pk).exists():
                blacklist.add(blocked_user)
            return HttpResponseRedirect('/profile/'+str(username)+'/')


class UnblockUserView(View):
    def get(self, request, username):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/')
        else:
            if User.objects.filter(username=username).first() is None:
                template = loader.get_template('UserProfile/user_not_found.html')
                return HttpResponse(template.render(dict(), request), status=404)
            blacklist = request.user.profile.blacklist
            blocked_user = User.objects.get(username=username)
            if blacklist.filter(pk=blocked_user.pk).exists():
                blacklist.remove(blocked_user)
            return HttpResponseRedirect('/profile/'+str(username)+'/')
