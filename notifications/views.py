from django.shortcuts import render, get_object_or_404
from django.template import loader
from .models import Notification
from django.http import HttpResponse
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class NotificationsList(View):
    def get(self, request):
        page = self.request.GET.get('page')
        unchecked_nots = Notification.objects.all()[::-1]
        paginator = Paginator(unchecked_nots, 20)

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