from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=110)
    description = models.TextField(blank=True)
    important = models.BooleanField(default=False, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    completed_date = models.DateTimeField(blank=True, null=True)

