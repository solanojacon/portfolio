from django import forms
from django.forms import inlineformset_factory, ModelForm, SelectDateWidget, Textarea
from .models import NoteLists, Notes

class ListForm(ModelForm):
    class Meta:
        model = NoteLists
        fields = '__all__'
        widgets = {
            'owner': forms.TextInput(attrs={'readonly': True}),
        }

class NoteForm(ModelForm):
    class Meta:
        model = Notes
        fields = '__all__'
        # fields = ['title']
        # exclude = ['owner']
        # visible_fields = ['title']
        # hidden_fields = ['owner']
        # labels = {
        #     'title': 'Note Title',
        # }
        widgets = {
            # 'note': Textarea(attrs={'cols': 40, 'rows': 10}),
            'owner': forms.TextInput(attrs={'readonly': True}),
            # 'owner': forms.TextInput(attrs={'disabled': True}),
        }
