from django import forms

from core.forms import ColorInput, OwnedModelForm

from .models import Subtask, Task, TaskList


class TaskListForm(OwnedModelForm):
    class Meta:
        model = TaskList
        fields = ['name', 'color']
        widgets = {'color': ColorInput()}


class TaskForm(OwnedModelForm):
    class Meta:
        model = Task
        fields = ['title', 'task_list', 'due_date', 'starred', 'completed', 'details']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'details': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only the user's own lists can be chosen; any other id fails validation.
        self.fields['task_list'].queryset = TaskList.objects.filter(owner=self.user)


class BaseSubtaskFormSet(forms.BaseInlineFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)
        if 'DELETE' in form.fields:
            form.fields['DELETE'].widget.attrs.update({'class': 'form-check-input', 'aria-label': 'Delete subtask'})


SubtaskFormSet = forms.inlineformset_factory(
    Task,
    Subtask,
    formset=BaseSubtaskFormSet,
    fields=['title', 'completed'],
    widgets={
        'title': forms.TextInput(attrs={'class': 'form-control', 'aria-label': 'Subtask title'}),
        'completed': forms.CheckboxInput(attrs={'class': 'form-check-input', 'aria-label': 'Subtask done'}),
    },
    extra=0,
    can_delete=True,
)
