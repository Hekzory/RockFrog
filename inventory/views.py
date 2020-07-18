from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from FirstVer.settings import TEMPLATES


# Create your views here.
class MyInventoryView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/auth/login')
        context = dict()
        template = loader.get_template("inventory/myinventory.html")
        return HttpResponse(template.render(context, request))
