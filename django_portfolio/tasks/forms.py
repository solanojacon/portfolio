from django import forms
from django.forms import inlineformset_factory, ModelForm, SelectDateWidget, Textarea
from .models import TaskLists, Tasks, Subtasks

class ListForm(ModelForm):
    class Meta:
        model = TaskLists
        fields = '__all__'
        widgets = {
            'owner': forms.TextInput(attrs={'readonly': True}),
        }

class TaskForm(ModelForm):
    class Meta:
        model = Tasks
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
        }
    def __init__(self, user, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['list'].queryset = TaskLists.objects.filter(owner__exact=user)
        self.fields['owner'].initial = user

class SubtaskForm(ModelForm):
    class Meta:
        model = Subtasks
        fields = '__all__'

SubtaskFormSet = inlineformset_factory(
    Tasks, Subtasks, form=SubtaskForm,
    extra=0, can_delete=True, can_delete_extra=True
)
