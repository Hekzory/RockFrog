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
        context = {'user' : user}
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

    def post(self, request):
        if not request.user.is_authenticated:
            print('asdasasdafasfasfasfafasgfjhg')
            return HttpResponseRedirect("/")
        else:
            bound_form = ProfileForm(request.POST)
            if bound_form.is_valid():
                bound_form.change_profile(request.user)
                template = loader.get_template('UserProfile/yourprofile.html')
                form = ProfileForm()
                context = {'form' : form}
                return HttpResponse(template.render(context, request))
            else:
                template = loader.get_template('UserProfile/yourprofile.html')
                form = ProfileForm()
                context = {'form' : form}
                return HttpResponse(template.render(context, request))
