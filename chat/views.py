from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
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
        return render(request, 'chat/base.html', None)


def post(request):
    if request.method == "POST":
        msg = request.POST.get('msgbox', None)
        if msg is not None:
            chat_message = Chat(user=request.user, message=msg)
            if msg != '':
                chat_message.save()
                
            return JsonResponse({'msg': msg, 'user': chat_message.user.username})
        else:
            return HttpResponse('Request must be not None.')
    else:
        return HttpResponse('Request must be POST.')


def messages(request):
    chat = Chat.objects.all()
    return render(request, 'chat/messages.html', {'chat': chat})
