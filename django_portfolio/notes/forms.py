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
    # def __init__(self, user=None, **kwargs):
    #     super(NoteForm, self).__init__(**kwargs)
    #     if user:
    #         self.fields['list'].queryset = NoteLists.objects.filter(owner=user)
    # def __init__(self, user, *args, **kwargs):
    #     super(NoteForm, self).__init__(*args, **kwargs)
    #     self.fields['list'].queryset = NoteLists.objects.filter(owner=user)
    #     self.fields['owner'].inicial = user
    def __init__(self, user=None, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
        if user!=None:
            self.fields['list'].queryset = NoteLists.objects.filter(owner__exact=user)
            self.fields['owner'].initial = user
