from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
import datetime
from django.utils import timezone

class ConversationMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_time = models.DateTimeField()

    def __str__(self):
        return self.text[:32]

    def is_earlier_24(self):
        return self.date_time > (timezone.now() - datetime.timedelta(days=1))


class Conversation(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')
    messages = models.ManyToManyField(ConversationMessage)
    last_interaction = models.DateTimeField(default=datetime.datetime.now)
    last_view_user1 = models.DateTimeField(default=datetime.datetime.now)
    last_view_user2 = models.DateTimeField(default=datetime.datetime.now)

    def update_interaction(self):
        self.last_interaction = datetime.datetime.now()
        self.save()

    def update_last_view_user1(self):
        self.last_view_user1 = datetime.datetime.now()
        self.save()

    def update_last_view_user2(self):
        self.last_view_user2 = datetime.datetime.now()
        self.save()

    def __str__(self):
        return "Conversation between "+str(self.user1)+" and "+str(self.user2)

    def get_last_message(self):
        if not self.is_empty():
            return self.messages.all().latest('date_time').text
        else:
            return "Возникла ошибка, пожалуйста, сообщите о ней администратору"

    def get_last_message_author(self):
        if not self.is_empty():
            return self.messages.all().latest('date_time').user.username
        else:
            return "Возникла ошибка, пожалуйста, сообщите о ней администратору"

    def is_empty(self):
        return len(self.messages.all()) == 0

    def get_last_message_date_time(self):
        if len(self.messages.all()) != 0:
            return self.messages.all().latest('date_time').date_time
        else:
            return None

    def get_messages_sorted_by_date(self):
        if len(self.messages.all()) != 0:
            return self.messages.all().order_by('date_time')
        else:
            return []


class ConversationList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    conversations = models.ManyToManyField(Conversation)


@receiver(post_save, sender=User)
def create_user_ConversationList(sender, instance, created=None, **kwargs):
    if created:
        ConversationList.objects.create(user=instance)
    else:
        instance.conversationlist.save()

def get_conversation_or_none(user_starter, user_target):
    current_conversation = None
    for conversation in user_starter.conversationlist.conversations.all():
        if conversation.user1.id == user_target.id or conversation.user2.id == user_target.id:
            current_conversation = conversation
    return conversation

def create_conversation(user_starter, user_target):
    new_conversation = Conversation(user1=user_starter, user2=user_target)
    new_conversation.save()
    user_starter.conversationlist.conversations.add(new_conversation)
    user_target.conversationlist.conversations.add(new_conversation)
    user_starter.conversationlist.save()
    user_target.conversationlist.save()
    return new_conversation
# Create your models here.
