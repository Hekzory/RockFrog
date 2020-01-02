from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

class ConversationMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_time = models.DateTimeField()

class Conversation(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')
    messages = models.ManyToManyField(ConversationMessage)

    def __str__(self):
        return "Conversation between "+str(self.user1)+" and "+str(self.user2)

    def get_last_message(self):
        if len(self.messages.all()) != 0:
            return self.messages.all().latest('date_time').text
        else:
            return "Сообщения отсутствуют"

    def get_last_message_date_time(self):
        if len(self.messages.all()) != 0:
            return self.messages.all().latest('date_time').date_time
        else:
            return ""

    def get_messages_sorted_by_date(self):
        if len(self.messages.all()) != 0:
            return self.messages.all().order_by('date_time')
        else:
            return []

class ConversationList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    conversations = models.ManyToManyField(Conversation)

@receiver(post_save, sender=User)
def create_user_ConversationList(sender, instance, created, **kwargs):
    if created:
        ConversationList.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_ConversationList(sender, instance, **kwargs):
    instance.ConversationList.save()

# Create your models here.
