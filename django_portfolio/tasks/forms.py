from django import forms
from django.forms import inlineformset_factory, ModelForm, SelectDateWidget, Textarea
from .models import List, Task, Subtask

class ListForm(ModelForm):
    class Meta:
        model = List
        fields = '__all__'
        widgets = {
            'owner': forms.TextInput(attrs={'readonly': True}),
        }

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        # fields = ['title']
        # exclude = ['owner']
        # visible_fields = ['title']
        # hidden_fields = ['owner']
        # labels = {
        #     'title': 'Task Title',
        # }
        widgets = {
            'details': Textarea(attrs={'cols': 40, 'rows': 10}),
            'date': SelectDateWidget(),
            'owner': forms.TextInput(attrs={'readonly': True}),
            # 'owner': forms.TextInput(attrs={'disabled': True}),
        }

class SubtaskForm(ModelForm):
    class Meta:
        model = Subtask
        fields = '__all__'

SubtaskFormSet = inlineformset_factory(
    Task, Subtask, form=SubtaskForm,
    extra=0, can_delete=True, can_delete_extra=True
)
