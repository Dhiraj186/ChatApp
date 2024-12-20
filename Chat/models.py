import datetime
from django.db import models
from django.contrib.auth.models import *

# Create your models here.
class Message(models.Model):
    toUser = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="toUser")
    fromUser = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="fromUser")
    message = models.TextField()
    date = models.DateTimeField(default=datetime.datetime.now)
    def __str__(self):
        return self.user