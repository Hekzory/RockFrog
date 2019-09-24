import datetime

from django.db import models
from django.utils import timezone


# Create your models here.
class Post(models.Model):
    post_text = models.TextField()
    post_name = models.CharField(max_length=200)
    post_date = models.DateTimeField('date published')
    post_announce = models.TextField()
    def __str__(self):
        return self.post_name
    def was_published_recently(self):
        return self.post_date >= timezone.now() - datetime.timedelta(days=1)
