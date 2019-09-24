from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse

# Create your views here.
def index(request):
    template = loader.get_template('mainapp/index.html')
    context = {}
    return HttpResponse(template.render(context, request))
