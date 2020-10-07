from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
import datetime
from django.utils import timezone


class DialogMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_time = models.DateTimeField()

    def __str__(self):
        return self.text[:32]

    def is_earlier_24(self):
        return self.date_time > (timezone.now() - datetime.timedelta(days=1))


class Dialog(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversation_owners')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversation_users')
    messages = models.ManyToManyField(DialogMessage)
    last_view = models.DateTimeField(default=datetime.datetime.now)
    last_interact = models.DateTimeField(default=datetime.datetime.now)

    def update_last_view(self):
        self.last_view = datetime.datetime.now()
        self.save()

    def update_last_interaction(self):
        self.last_interact = datetime.datetime.now()
        self.save()

    def __str__(self):
        return "Conversation between " + str(self.owner) + " and " + str(self.user)

    def get_last_message(self):
        if self.is_empty():
            return "Сообщения отсутствуют"
        return self.messages.all().latest('date_time')

    def is_empty(self):
        return len(self.messages.all()) == 0

    def get_last_message_time(self):
        if len(self.messages.all()) != 0:
            return self.messages.all().latest('date_time').date_time
        else:
            return None

    def get_messages_sorted_by_date(self):
        if not self.is_empty():
            return self.messages.all().order_by('date_time')
        else:
            return []


class DialogList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="dialog_list")
    dialogs = models.ManyToManyField(Dialog)


@receiver(post_save, sender=User)
def create_user_dialog_list(sender, instance, created=None, **kwargs):
    if created:
        DialogList.objects.create(user=instance)
    else:
        try:
            instance.dialog_list.save()
        except DialogList.DoesNotExist:
            DialogList.objects.create(user=instance)


def create_dialog(owner, user):
    new_dialog = Dialog.objects.create(owner=owner, user=user)
    new_dialog.save()
    owner.dialog_list.dialogs.add(new_dialog)
    return new_dialog

def add_message_to_dialog(user1, user2, message):
    try:
        dialog1 = user1.dialog_list.dialogs.get(user=user2)
    except Dialog.DoesNotExist:
        dialog1 = create_dialog(user1, user2)
    try:
        dialog2 = user2.dialog_list.dialogs.get(user=user1)
    except Dialog.DoesNotExist:
        dialog2 = create_dialog(user2, user1)
    dialog1.messages.add(message)
    dialog2.messages.add(message)
    dialog1.update_last_view()
    dialog1.update_last_interaction()
    dialog2.update_last_interaction()
# Create your models here.
