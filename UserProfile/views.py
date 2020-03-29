from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.template import loader
from django.contrib.auth.models import User
from django.views.generic import View
from .forms import ProfileForm
# Create your views here.
def index(request):
    if request.user.is_authenticated:
        template = loader.get_template('UserProfile/yourprofile.html')
        context = {'user' : request.user}
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect("/")

def userprofile(request, username):
    if request.user.is_authenticated:
        template = loader.get_template('UserProfile/userprofile.html')
        if User.objects.filter(username=username).count() != 0:
            user = User.objects.filter(username=username)[0]
        else:
            return HttpResponseNotFound("User not found")
        context = {'user' : user}
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template('UserProfile/userprofile.html')
        if User.objects.filter(username=username).count() != 0:
            user = User.objects.filter(username=username)[0]
        else:
            return HttpResponseNotFound("User not found")
        context = {'user': user}
        return HttpResponse(template.render(context, request))


class ProfileView(View):
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
            initial_params['about']= request.user.profile.about
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
            print(list(request.POST.items()))
            check = bound_form.is_valid()
            if check:
                bound_form.change_profile(request.user, request.FILES)
                template = loader.get_template('UserProfile/editprofile.html')
                form = ProfileForm()
                context = {'form': form}
                return HttpResponse(template.render(context, request))
            else:
                template = loader.get_template('UserProfile/editprofile.html')
                context = {'form': bound_form}
                return HttpResponse(template.render(context, request))