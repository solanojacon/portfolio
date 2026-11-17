from django import forms

from core.forms import ColorInput, OwnedModelForm

from .models import Note, NoteList


class NoteListForm(OwnedModelForm):
    class Meta:
        model = NoteList
        fields = ['name', 'color']
        widgets = {'color': ColorInput()}


class NoteForm(OwnedModelForm):
    class Meta:
        model = Note
        fields = ['title', 'note_list', 'starred', 'content']
        widgets = {'content': forms.Textarea(attrs={'rows': 10})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only the user's own lists can be chosen; any other id fails validation.
        self.fields['note_list'].queryset = NoteList.objects.filter(owner=self.user)
