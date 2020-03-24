from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from chat.models import Chat
from notifications.models import Notificationlist, Notification


def home(request):
    chats = Chat.objects.all()
    ctx = {
        'home': 'active',
        'chat': chats
    }
    if request.user.is_authenticated:
        return render(request, 'chat/chat.html', ctx)
    else:
        return render(request, 'chat/base.html', ctx)


def messages(request):
    chat = Chat.objects.all()
    return render(request, 'chat/messages.html', {'chat': chat})
