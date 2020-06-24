from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


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

    def __str__(self):
        return self.user.username


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



