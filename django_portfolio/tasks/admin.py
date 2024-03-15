from django.contrib import admin
from .models import TaskLists, Tasks, Subtasks

admin.site.register(TaskLists)
admin.site.register(Tasks)
admin.site.register(Subtasks)
