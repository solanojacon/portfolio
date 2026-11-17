from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone

from core.forms import validate_hex_color


class TaskList(models.Model):
    name = models.CharField(max_length=25)
    color = models.CharField(max_length=7, default='#FFFFFF', validators=[validate_hex_color])
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='task_lists')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tasks:list_update', args=[self.pk])


class Task(models.Model):
    title = models.CharField(max_length=100)
    task_list = models.ForeignKey(TaskList, on_delete=models.CASCADE, related_name='tasks', verbose_name='list')
    due_date = models.DateField(null=True, blank=True)
    starred = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    details = models.TextField(blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')

    class Meta:
        # Open tasks first, then by due date (tasks without one last).
        ordering = ['completed', models.F('due_date').asc(nulls_last=True), 'title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tasks:update', args=[self.pk])

    @property
    def is_overdue(self):
        return self.due_date is not None and not self.completed and self.due_date < timezone.localdate()


class Subtask(models.Model):
    title = models.CharField(max_length=100)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return self.title
