from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.template import loader
from django.contrib.auth.models import User

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
