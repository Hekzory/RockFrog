from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import *
import datetime


class DialogPage(View):
    def get(self, request, user_id):
        context = dict()
        if request.user.is_authenticated:
            try:
                user_messaging_with = User.objects.get(pk=user_id)
                context['user_messaging_with'] = user_messaging_with
            except ObjectDoesNotExist:
                return HttpResponseRedirect('/conversations')
            current_conversation = None
            # Ищем переписку с нужным пользователем
            for conversation in request.user.conversationlist.conversations.all():
                if conversation.user1.id == user_messaging_with.id or conversation.user2.id == user_messaging_with.id:
                    current_conversation = conversation
            if current_conversation == None:
                # Если переписки не существует, отображаем окно без сообщений. После отправки первого сообщения
                # Создастся объект переписки, не раньше.
                context['messages'] = []
                context['conversation_id'] = 0
            else:
                # Если переписка существует, обновляем время последнего просмотра переписки для нужного пользователя
                if current_conversation.user1.id == request.user.id:
                    current_conversation.update_last_view_user1()
                else:
                    current_conversation.update_last_view_user2()
                context['messages'] = current_conversation.get_messages_sorted_by_date()
                context['conversation_id'] = current_conversation.pk
            return render(request, 'personal_messages/base.html', context)
        else:
            return HttpResponseRedirect('/auth/login')

class DialogsList(View):
    def get(self, request):
        context = dict()
        if request.user.is_authenticated:
            context['conversationlist'] = request.user.conversationlist.conversations.all().order_by('last_interaction')[::-1]
            users_messaging_with = []
            unread_messages = []
            for i in context['conversationlist']:
                if request.user.id == i.user1.id:
                    unread_messages.append(i.messages.filter(date_time__gt=i.last_view_user1).count())
                    users_messaging_with.append(i.user2)
                elif request.user.id == i.user2.id:
                    unread_messages.append(i.messages.filter(date_time__gt=i.last_view_user2).count())
                    users_messaging_with.append(i.user1)
            context['users_messaging_with'] = users_messaging_with
            context['conversations'] = [[users_messaging_with[i], context['conversationlist'][i], unread_messages[i]] for i in range(len(users_messaging_with))]
            return render(request, 'personal_messages/dialog_list.html', context)
        else:
            return HttpResponseRedirect('/auth/login')

class DialogsListBase(View):
    def get(self, request):
        context = dict()
        if request.user.is_authenticated:
            context['conversationlist'] = request.user.conversationlist.conversations.all().order_by('last_interaction')[::-1]
            users_messaging_with = []
            unread_messages = []
            for i in context['conversationlist']:
                if request.user.id == i.user1.id:
                    unread_messages.append(i.messages.filter(date_time__gt=i.last_view_user1).count())
                    users_messaging_with.append(i.user2)
                elif request.user.id == i.user2.id:
                    unread_messages.append(i.messages.filter(date_time__gt=i.last_view_user2).count())
                    users_messaging_with.append(i.user1)
            context['users_messaging_with'] = users_messaging_with
            context['conversations'] = [[users_messaging_with[i], context['conversationlist'][i], unread_messages[i]] for i in range(len(users_messaging_with))]
            return render(request, 'personal_messages/dialog_list_base.html', context)
        else:
            return HttpResponseRedirect('/auth/login')

# Create your views here.
