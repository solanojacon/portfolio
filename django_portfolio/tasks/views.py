from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from .models import TaskLists, Tasks
from .forms import ListForm, TaskForm, SubtaskFormSet


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())


@login_required
def test(request):
    template = loader.get_template('tasks_test.html')
    context = {
        'fruits_data': ['Apple', 'Banana', 'Cherry'],
    }
    return HttpResponse(template.render(context, request))


@login_required
def lists(request):
    superuser = request.user.is_superuser
    if superuser == True:
        lists_data = TaskLists.objects.all()
    else:
        lists_data = TaskLists.objects.filter(owner__exact=request.user.id)
    paginator = Paginator(lists_data, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'lists_data': lists_data,
        'superuser': superuser,
        'page_obj': page_obj,
    }
    return render(request, 'tasks_lists.html', context)


@login_required
def add_list(request):
    form = ListForm(initial={'owner': request.user.id})
    if request.method=='POST':
        form = ListForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks:lists')
    context = {'form': form}
    return render(request, 'tasks_add_list.html', context)


@login_required
def edit_list(request, pk):
    lists_data = get_object_or_404(TaskLists, pk=pk)
    form = ListForm(instance=lists_data)
    if request.method=='POST':
        form = ListForm(request.POST, instance=lists_data)
        if form.is_valid():
            form.save()
            return redirect('tasks:lists')
    context = {'form': form}
    return render(request, 'tasks_edit_list.html', context)


@login_required
def delete_list(request, pk):
    lists_data = get_object_or_404(TaskLists, pk=pk)
    lists_data.delete()
    return redirect('tasks:lists')


class TaskList(LoginRequiredMixin, ListView):
    paginate_by = 10
    def get_queryset(self):
        superuser = self.request.user.is_superuser
        if superuser == True:
            return Tasks.objects.all()
        else:
            return Tasks.objects.filter(owner__exact=self.request.user.id)
    template_name = "tasks_tasks.html"
    context_object_name = "tasks_data"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['superuser'] = self.request.user.is_superuser
        return context


class TaskInline(LoginRequiredMixin):
    form_class = TaskForm
    model = Tasks
    template_name = "tasks_add_edit_task.html"

    def form_valid(self, form):
        if form.instance.owner is None:
            form.instance.owner = self.request.user
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))
        self.object = form.save()
        # for every formset, attempt to find a specific formset save function
        # otherwise, just save.
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('tasks:tasks')

    def formset_subtasks_valid(self, formset):
        """
        Hook for custom formset saving.Useful if you have multiple formsets
        """
        subtasks = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this 2 lines, if you have can_delete=True parameter 
        # set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for subtask in subtasks:
            subtask.task = self.object
            subtask.save()


class TaskCreate(TaskInline, CreateView):

    def get_context_data(self, **kwargs):
        context = super(TaskCreate, self).get_context_data(**kwargs)
        context['named_formsets'] = self.get_named_formsets()
        context['label'] = {'task_title': 'Task - Add', 'subtask_title': 'Subtask - Add', 'submit_button': 'Add Task'}
        return context

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'subtasks': SubtaskFormSet(prefix='subtasks'),
            }
        else:
            return {
                'subtasks': SubtaskFormSet(self.request.POST or None, self.request.FILES or None, prefix='subtasks'),
            }


class TaskUpdate(TaskInline, UpdateView):

    def get_context_data(self, **kwargs):
        context = super(TaskUpdate, self).get_context_data(**kwargs)
        context['named_formsets'] = self.get_named_formsets()
        context['label'] = {'task_title': 'Task - Edit', 'subtask_title': 'Subtask - Edit', 'submit_button': 'Save Changes'}
        return context

    def get_named_formsets(self):
        return {
            'subtasks': SubtaskFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='subtasks'),
        }


@login_required
def delete_task(request, pk):
    tasks_data = get_object_or_404(Tasks, pk=pk)
    tasks_data.delete()
    return redirect('tasks:tasks')


# '''This function is for custom added delete button functionality. If you don't want to use custom delete buttons than don't add this'''

# @login_required
# def delete_subtask(request, pk):
#     try:
#         subtask = Subtasks.objects.get(id=pk)
#     except Subtask.DoesNotExist:
#         messages.success(
#             request, 'Object Does not exit'
#             )
#         return redirect('tasks:update_task', pk=subtask.task.id)

#     subtask.delete()
#     messages.success(
#             request, 'Subtask deleted successfully'
#             )
#     return redirect('tasks:update_task', pk=subtask.task.id)
