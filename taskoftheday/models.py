from __future__ import unicode_literals
from django.contrib import admin

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Guide(models.Model):
    name = models.CharField(max_length=200)
    guide_category = models.CharField(max_length=70)
    guide_why = models.TextField()
    guide_how = models.TextField()
    is_complete = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class Step(models.Model):
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE)
    sequence_number = models.PositiveIntegerField(default=1)
    name = models.CharField(max_length=10)
    is_complete = models.BooleanField(default=False)

    class Meta:
        unique_together = ("guide", "sequence_number")

    def __unicode__(self):
        return self.name


class Task(models.Model):
    step = models.ForeignKey(Step, on_delete=models.CASCADE)
    sequence_number = models.CharField(max_length=10, default='1')
    name = models.CharField(max_length=10)
    task_img = models.ImageField(upload_to='static/taskoftheday/img/uploads-tasks', blank=True)
    task_task = models.TextField()
    task_description = models.TextField()
    is_complete = models.BooleanField(default=False)

    class Meta:
        unique_together = ("step", "sequence_number")

    def __unicode__(self):
        return self.sequence_number


class UserTaskHistory(models.Model):
    user = models.ForeignKey(User, null=True)
    guide = models.ForeignKey(Guide, null=True)
    step = models.ForeignKey(Step, null=True)
    task = models.ForeignKey(Task, null=True)
    is_complete = models.BooleanField(default=False)
    completion_datetime = models.DateTimeField()
