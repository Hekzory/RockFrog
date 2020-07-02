from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, date, timezone, timedelta
import locale



def user_directorypath(instance, filename):
    return 'user{0}/{1}'.format(instance.user.id, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    email = models.TextField(max_length=50, blank=True)
    city = models.TextField(max_length=30, blank=True)
    phone = models.TextField(max_length=30, blank=True)
    interests = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to=user_directorypath, default='/static/profile.jpg')
    blacklist = models.ManyToManyField(User, related_name='blacklists')
    verified = models.BooleanField(default=False)
    last_time_online = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.user.username

    def last_online_update(self):
        self.last_time_online = datetime.now()
        self.save()

    def online_status(self):
        now = datetime.now(timezone.utc) + timedelta(hours=3)
        last_online = self.last_time_online + timedelta(hours=3)
        t = (now - last_online).total_seconds()
        if t <= 600:
            return 'Онлайн'
        elif t <= 3000:
            return 'Был в сети ' + str(int(t//60)) + ' мин. назад'
        elif t <= 5400:
            return 'Был в сети час назад'
        if now.date() == last_online.date():
            seconds_from_midnight = (last_online - last_online.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
            current_time = ':'.join(str(timedelta(seconds=seconds_from_midnight)).split(':')[:2])
            return 'Был в сети сегодня, ' + current_time
        elif t <= 86400:
            seconds_from_midnight = (last_online - last_online.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
            current_time = ':'.join(str(timedelta(seconds=seconds_from_midnight)).split(':')[:2])
            return 'Был в сети вчера, ' + current_time
        else:
            seconds_from_midnight = (last_online - last_online.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
            current_time = ':'.join(str(timedelta(seconds=seconds_from_midnight)).split(':')[:2])
            locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")
            current_day_month = last_online.strftime("%d %b")
            return 'Был в сети ' + current_day_month + ' в ' + current_time


class PrivacySettings(models.Model):
    allow_to_view_for_unreg = models.BooleanField(default=True)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=Profile)
def create_privacy_settings(sender, instance, created, **kwargs):
    if created:
        PrivacySettings.objects.create(profile=instance)



