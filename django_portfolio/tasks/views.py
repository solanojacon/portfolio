from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, FormMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from django.urls import reverse
from django.utils.decorators import method_decorator
from .models import TaskLists, Tasks
from .forms import ListForm, TaskForm, SubtaskFormSet

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

@login_required
def test(request):
    template = loader.get_template('test.html')
    context = {
        'fruits_data': ['Apple', 'Banana', 'Cherry'],
    }
    return HttpResponse(template.render(context, request))

# @login_required
# def tasks(request):
#     superuser = request.user.is_superuser
#     if superuser == True:
#         tasks_data = Tasks.objects.all()
#     else:
#         tasks_data = Tasks.objects.filter(owner__exact=request.user.id)
#     context = {
#         'tasks_data': tasks_data,
#         'superuser': superuser,
#     }
#     return render(request, 'tasks.html', context) # render is a shortcut for HttpResponse

# @login_required
# def add_task(request):
#     form = TaskForm(initial={'owner': request.user.id})
#     if request.method=='POST':
#         form = TaskForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('tasks:tasks')
#     context = {'form': form}
#     return render(request, 'add_task.html', context)

# @login_required
# def edit_task(request, pk):
#     tasks_data = get_object_or_404(Tasks, pk=pk)
#     form = TaskForm(instance=tasks_data)
#     if request.method=='POST':
#         form = TaskForm(request.POST, instance=tasks_data)
#         if form.is_valid():
#             form.save()
#             return redirect('tasks:tasks')
#     context = {'form': form}
#     return render(request, 'edit_task.html', context)

@login_required
def delete_task(request, pk):
    tasks_data = get_object_or_404(Tasks, pk=pk)
    tasks_data.delete()
    return redirect('tasks:tasks')

@login_required
def lists(request):
    superuser = request.user.is_superuser
    if superuser == True:
        lists_data = TaskLists.objects.all()
    else:
        lists_data = TaskLists.objects.filter(owner__exact=request.user.id)
    context = {
        'lists_data': lists_data,
        'superuser': superuser,
    }
    return render(request, 'lists.html', context)

@login_required
def add_list(request):
    form = ListForm(initial={'owner': request.user.id})
    if request.method=='POST':
        form = ListForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks:lists')
    context = {'form': form}
    return render(request, 'add_list.html', context)

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
    return render(request, 'edit_list.html', context)

@login_required
def delete_list(request, pk):
    lists_data = get_object_or_404(TaskLists, pk=pk)
    lists_data.delete()
    return redirect('tasks:lists')



class TaskList(LoginRequiredMixin, ListView):
    def get_queryset(self):
        superuser = self.request.user.is_superuser
        if superuser == True:
            return Tasks.objects.all()
        else:
            return Tasks.objects.filter(owner__exact=self.request.user.id)
    template_name = "tasks.html"
    context_object_name = "tasks_data"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['superuser'] = self.request.user.is_superuser
        return context



class TaskInline(LoginRequiredMixin):
    form_class = TaskForm
    model = Tasks
    template_name = "add_edit_task.html"

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



# '''This function is for custom added delete button functionality. If you don't want to use custom delete buttons than don't add this'''


# @login_required
# def delete_subtask(request, pk):
#     try:
#         subtask = Subtasks.objects.get(id=pk)
#     except Subtask.DoesNotExist:
#         messages.success(
#             request, 'Object Does not exit'
#             )
#         return redirect('tasks:update_task', pk=subtask.task.id) # REVISAR!!!

#     subtask.delete()
#     messages.success(
#             request, 'Subtask deleted successfully'
#             )
#     return redirect('tasks:update_task', pk=subtask.task.id) # REVISAR!!!
