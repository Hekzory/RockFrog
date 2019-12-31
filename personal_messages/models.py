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
