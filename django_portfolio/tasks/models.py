from datetime import date
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

class TaskLists(models.Model):
    name = models.CharField(max_length=25, blank=False, null=False)
    color = models.CharField(max_length=7, default='#FFFFFF', blank=False, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    class Meta:
        ordering = ['owner', 'name']
    def get_absolute_url(self):
        return reverse('tasks:edit_list', args=[str(self.id)])
    def __str__(self):
        return f'{self.name}'

class Tasks(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    list = models.ForeignKey(TaskLists, on_delete=models.CASCADE, blank=False, null=False)
    date = models.DateField(blank=True, null=True)
    starred = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    details = models.CharField(max_length=1000, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    class Meta:
        ordering = ['owner', 'list', 'title']
    def get_absolute_url(self):
        return reverse('tasks:edit_task', args=[str(self.id)])
    def __str__(self):
        return f'{self.owner} | {self.list} | {self.title}'
    @property
    def is_overdue(self):
        return bool(self.date and date.today() > self.date and self.completed == False)

class Subtasks(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE, blank=False, null=False)
    completed = models.BooleanField(default=False)
    class Meta:
        ordering = ['task', 'title']
    def get_absolute_url(self):
        return reverse('tasks:edit_subtask', args=[str(self.id)])
    def __str__(self):
        return f'{self.task} | {self.title}'
