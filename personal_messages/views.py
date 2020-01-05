from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .forms import *
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
            send_message_form = SendPMForm()
            context['send_pm_form'] = send_message_form
            current_conversation = None
            for conversation in request.user.conversationlist.conversations.all():
                if conversation.user1.id == user_messaging_with.id or conversation.user2.id == user_messaging_with.id:
                    current_conversation = conversation
            if current_conversation == None:
                messages = []
                context['conversation_id'] = 0
            else:
                messages = current_conversation.get_messages_sorted_by_date()
                context['conversation_id'] = current_conversation.pk
            context['messages'] = messages
            return render(request, 'personal_messages/base.html', context)
        else:
            return HttpResponseRedirect('/auth/login')
    def post(self, request, user_id):
        context = dict()
        if request.user.is_authenticated:
            #Получаем пользователей
            user = request.user
            try:
                user_messaging_with = User.objects.get(pk=user_id)
                context['user_messaging_with'] = user_messaging_with
            except ObjectDoesNotExist:
                return HttpResponseRedirect('/conversations')

            send_message_form = SendPMForm(request.POST)
            context['send_pm_form'] = SendPMForm()
            #Проверяем, переписывались ли пользователи до этого
            current_conversation = None
            for conversation in request.user.conversationlist.conversations.all():
                if conversation.user1.id == user_messaging_with.id or conversation.user2.id == user_messaging_with.id:
                    current_conversation = conversation
            # Если форма отправлена правильно
            if send_message_form.is_valid():
                new_conversation_message = ConversationMessage(user=user, text=send_message_form.cleaned_data['text'],
                                                               date_time=datetime.datetime.now())
                new_conversation_message.save()
                #Если до этого не переписывались, создаем переписку
                if current_conversation == None:
                    new_conversation = Conversation(user1=user, user2=user_messaging_with)
                    new_conversation.save()
                    new_conversation.messages.add(new_conversation_message)
                    new_conversation.save()
                    user.conversationlist.conversations.add(new_conversation)
                    user_messaging_with.conversationlist.conversations.add(new_conversation)
                    current_conversation = new_conversation
                else:
                    current_conversation.messages.add(new_conversation_message)

            messages = current_conversation.get_messages_sorted_by_date()
            context['messages'] = messages
            return render(request, 'personal_messages/base.html', context)
        else:
            return HttpResponseRedirect('/auth/login')

class DialogsList(View):
    def get(self, request):
        context = dict()
        if request.user.is_authenticated:
            print(dir(request.user))
            context['conversationlist'] = request.user.conversationlist.conversations.all()
            print(context['conversationlist'])
            users_messaging_with = []
            for i in context['conversationlist']:
                if request.user.id == i.user1.id:
                    users_messaging_with.append(i.user2)
                elif request.user.id == i.user2.id:
                    users_messaging_with.append(i.user1)
            context['users_messaging_with'] = users_messaging_with
            context['conversations'] = [[users_messaging_with[i],context['conversationlist'][i]] for i in range(len(users_messaging_with))]
            return render(request, 'personal_messages/dialog_list.html', context)
        else:
            return HttpResponseRedirect('/auth/login')

# Create your views here.
