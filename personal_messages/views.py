from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class DialogPage(View):
    def get(self, request, user_id):
        context = dict()
        if request.user.is_authenticated:
            try:
                user = User.objects.get(pk=user_id)
                print(user, "GOT")
                context['user'] = user
            except ObjectDoesNotExist:
                return HttpResponseRedirect('/conversations')
            return render(request, 'personal_messages/base.html', context)
        else:
            return HttpResponseRedirect('/auth/login')

class DialogsList(View):
    def get(self, request):
        context = dict()
        if request.user.is_authenticated:
            return render(request, 'personal_messages/dialog_list.html', context)
        else:
            return HttpResponseRedirect('/auth/login')

# Create your views here.
