from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.db.models import Count, Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from core.mixins import OwnerFormMixin, OwnerQuerysetMixin

from .forms import SubtaskFormSet, TaskForm, TaskListForm
from .models import Task, TaskList

# Tasks


class TaskIndexView(OwnerQuerysetMixin, ListView):
    model = Task
    paginate_by = 20
    template_name = 'tasks/task_index.html'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('task_list').annotate(
            subtask_count=Count('subtasks'),
            subtask_done=Count('subtasks', filter=Q(subtasks__completed=True)),
        ).order_by(*Task._meta.ordering)  # aggregation drops the default ordering
        self.selected_list = None
        list_id = self.request.GET.get('list', '')
        if list_id.isdigit():
            self.selected_list = TaskList.objects.filter(owner=self.request.user, pk=list_id).first()
            if self.selected_list:
                queryset = queryset.filter(task_list=self.selected_list)
        return queryset

    def get_context_data(self, **kwargs):
        return super().get_context_data(selected_list=self.selected_list, **kwargs)


class TaskFormMixin(OwnerFormMixin, SuccessMessageMixin):
    """Saves a task together with its subtasks, in one transaction."""

    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:index')

    def get_subtasks(self, form):
        data = self.request.POST if self.request.method == 'POST' else None
        return SubtaskFormSet(data, instance=form.instance, prefix='subtasks')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault('subtasks', self.get_subtasks(context['form']))
        return context

    def form_valid(self, form):
        subtasks = self.get_subtasks(form)
        if not subtasks.is_valid():
            return self.render_to_response(self.get_context_data(form=form, subtasks=subtasks))
        with transaction.atomic():
            response = super().form_valid(form)
            subtasks.instance = self.object
            subtasks.save()
        return response


class TaskCreateView(TaskFormMixin, CreateView):
    success_message = 'Task "%(title)s" added.'
    extra_context = {'title': 'New task'}

    def get(self, request, *args, **kwargs):
        if not TaskList.objects.filter(owner=request.user).exists():
            messages.info(request, 'Create a task list first, then add tasks to it.')
            return redirect('tasks:list_create')
        return super().get(request, *args, **kwargs)

    def get_initial(self):
        # Coming from a filtered task list, preselect that list.
        initial = super().get_initial()
        list_id = self.request.GET.get('list', '')
        if list_id.isdigit():
            initial['task_list'] = list_id
        return initial


class TaskUpdateView(OwnerQuerysetMixin, TaskFormMixin, UpdateView):
    success_message = 'Task "%(title)s" saved.'
    extra_context = {'title': 'Edit task'}


class TaskDeleteView(OwnerQuerysetMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('tasks:index')
    success_message = 'Task deleted.'
    extra_context = {'title': 'Delete task', 'cancel_url': reverse_lazy('tasks:index')}


# Task lists


class TaskListIndexView(OwnerQuerysetMixin, ListView):
    model = TaskList
    paginate_by = 20
    template_name = 'tasks/tasklist_index.html'

    def get_queryset(self):
        return super().get_queryset().annotate(
            task_count=Count('tasks'),
            open_count=Count('tasks', filter=Q(tasks__completed=False)),
        ).order_by('name')  # aggregation drops the default ordering


class TaskListCreateView(OwnerFormMixin, SuccessMessageMixin, CreateView):
    model = TaskList
    form_class = TaskListForm
    template_name = 'form.html'
    success_url = reverse_lazy('tasks:list_index')
    success_message = 'List "%(name)s" created.'
    extra_context = {'title': 'New task list', 'cancel_url': reverse_lazy('tasks:list_index')}


class TaskListUpdateView(OwnerQuerysetMixin, OwnerFormMixin, SuccessMessageMixin, UpdateView):
    model = TaskList
    form_class = TaskListForm
    template_name = 'form.html'
    success_url = reverse_lazy('tasks:list_index')
    success_message = 'List "%(name)s" saved.'
    extra_context = {'title': 'Edit task list', 'cancel_url': reverse_lazy('tasks:list_index')}


class TaskListDeleteView(OwnerQuerysetMixin, SuccessMessageMixin, DeleteView):
    model = TaskList
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('tasks:list_index')
    success_message = 'List deleted.'
    extra_context = {'title': 'Delete task list', 'cancel_url': reverse_lazy('tasks:list_index')}

    def get_context_data(self, **kwargs):
        count = self.object.tasks.count()
        if count:
            kwargs['warning'] = f'Its {count} task{"s" if count != 1 else ""} will be deleted too.'
        return super().get_context_data(**kwargs)
