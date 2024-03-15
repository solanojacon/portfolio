from django.contrib import admin
from .models import List, Task, Subtask

admin.site.register(List)
admin.site.register(Task)
admin.site.register(Subtask)
