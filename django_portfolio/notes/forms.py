from django import forms
from django.forms import ModelForm
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
        widgets = {
            'owner': forms.TextInput(attrs={'readonly': True}),
        }
