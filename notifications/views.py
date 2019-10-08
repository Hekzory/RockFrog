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
            new_notifications = Notificationlist.objects.all().filter(user = request.user)[0].notifications.filter(not_checked = True)[::-1]
            old_notifications = Notificationlist.objects.all().filter(user = request.user)[0].notifications.filter(not_checked = False)[::-1]
            all_notifications = new_notifications + old_notifications

            paginator = Paginator(all_notifications, 4)

            try:
                notifications = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                notifications = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                notifications = paginator.page(paginator.num_pages)

            template = loader.get_template('notifications/index.html')
            context = {
                'notifications': notifications,
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
