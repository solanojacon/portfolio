from django.contrib import admin

from .models import Subtask, Task, TaskList


@admin.register(TaskList)
class TaskListAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'color']
    list_filter = ['owner']
    search_fields = ['name']


class SubtaskInline(admin.TabularInline):
    model = Subtask
    extra = 0


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'task_list', 'owner', 'due_date', 'starred', 'completed']
    list_filter = ['completed', 'starred', 'owner']
    search_fields = ['title', 'details']
    inlines = [SubtaskInline]
