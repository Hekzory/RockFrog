from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.template import loader
from .models import *
import datetime


class DialogPage(View):
    def get(self, request, user_id):
        context = dict()
        context['current_app_name'] = "personal_messages"
        if request.user.is_authenticated:
            request.user.profile.last_online_update()
            try:
                user_messaging_with = User.objects.get(pk=user_id)
                context['user_messaging_with'] = user_messaging_with
            except ObjectDoesNotExist:
                # Если пользователь не был найден, отображаем страницу об ошибке
                template = loader.get_template('personal_messages/user_not_found.html')
                return HttpResponse(template.render(context, request), status=404)
            # Если пользователь пытается пообщаться с самим собой, посылаем его
            if request.user.id == user_id:
                return HttpResponseRedirect('/conversations')
            current_conversation = None
            # Ищем переписку с нужным пользователем
            for conversation in request.user.conversationlist.conversations.all():
                if conversation.user1.id == user_messaging_with.id or conversation.user2.id == user_messaging_with.id:
                    current_conversation = conversation
            if current_conversation == None:
                # Если переписки не существует, отображаем окно без сообщений. После просмотра
                # Создастся объект переписки
                current_conversation = create_conversation(request.user, user_messaging_with)
            # Обновляем время последнего просмотра переписки для нужного пользователя
            if current_conversation.user1.id == request.user.id:
                current_conversation.update_last_view_user1()
            else:
                current_conversation.update_last_view_user2()
            context['messages'] = current_conversation.get_messages_sorted_by_date()
            context['conversation_id'] = current_conversation.pk
            # Проверка на наличие в чёрных списках
            context["is_viewer_blacklisted"] = False
            context["is_viewed_blacklisted"] = False
            if user_messaging_with.profile.blacklist.filter(pk=request.user.pk).exists():
                context["is_viewer_blacklisted"] = True
            if request.user.profile.blacklist.filter(pk=user_messaging_with.pk).exists():
                context["is_viewed_blacklisted"] = True
            return render(request, 'personal_messages/base.html', context)
        else:
            return HttpResponseRedirect('/auth/login')

class DialogsList(View):
    def get(self, request):
        context = dict()
        context['current_app_name'] = "personal_messages"
        if request.user.is_authenticated:
            print(dir(request))
            print(request.scope)
            return render(request, 'personal_messages/aero/dialog_list.html', context)
        else:
            return HttpResponseRedirect('/auth/login')

    #Код, работающий со старым дизайном сайта
    def get_deprecated(self, request):
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
        context['current_app_name'] = "personal_messages"
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

class DeleteMessage(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/')
        request.user.profile.last_online_update()
        try:
            message = ConversationMessage.objects.get(id=request.POST["message_id"])
        except ConversationMessage.DoesNotExist:
            return JsonResponse({"response": "DoesNotExist"})
        except ValueError:
            return JsonResponse({"response": "IdNotADigit"})
        if message.is_earlier_24() and message.user.id == request.user.id:
            message.delete()
            return JsonResponse({"response":"ok"})
        else:
            return JsonResponse({"response": "error"})

class EditMessage(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/')
        request.user.profile.last_online_update()
        try:
            message = ConversationMessage.objects.get(id=int(request.POST["message_id"]))
        except ConversationMessage.DoesNotExist:
            return JsonResponse({"response": "DoesNotExist"})
        except ValueError:
            return JsonResponse({"response": "IdNotADigit"})
        if message.is_earlier_24() and message.user.id == request.user.id and request.POST["message"].strip() != "":
            message.text = request.POST["message"]
            message.save()
            return JsonResponse({"response":"ok"})
        else:
            return JsonResponse({"response": "error"})
