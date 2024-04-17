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
    def __init__(self, user=None, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
        if user!=None:
            if user.is_superuser:
                self.fields['list'].queryset = NoteLists.objects.all()
            else:
                self.fields['list'].queryset = NoteLists.objects.filter(owner__exact=user)
            self.fields['owner'].initial = user
