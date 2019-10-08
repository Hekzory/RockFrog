from django.shortcuts import render, get_object_or_404
from django.template import loader
from .models import Notification, Notificationlist
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse


class NotificationsList(View):
    def get(self, request):
        if request.user.is_authenticated:
            page = self.request.GET.get('page')
            all_nots = Notificationlist.objects.all().filter(user = request.user)[0].notifications.all()[::-1]
            paginator = Paginator(all_nots, 4)

            try:
                nots = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                nots = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                nots = paginator.page(paginator.num_pages)

            template = loader.get_template('notifications/index.html')
            context = {
                'notifications': nots,
            }
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponseRedirect("/auth/login")

    def post(self, request):
        temp_id = int(request.POST.get('not_id', None))
        notification = Notificationlist.objects.all().filter(user = request.user)[0].notifications.all().filter(id = temp_id)[0]
        notification.not_checked = False
        notification.save()
        return HttpResponseRedirect("/notifications/")
