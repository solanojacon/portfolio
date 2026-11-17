from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from core.mixins import OwnerFormMixin, OwnerQuerysetMixin

from .forms import NoteForm, NoteListForm
from .models import Note, NoteList

# Notes


class NoteIndexView(OwnerQuerysetMixin, ListView):
    model = Note
    paginate_by = 20
    template_name = 'notes/note_index.html'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('note_list')
        self.selected_list = None
        list_id = self.request.GET.get('list', '')
        if list_id.isdigit():
            self.selected_list = NoteList.objects.filter(owner=self.request.user, pk=list_id).first()
            if self.selected_list:
                queryset = queryset.filter(note_list=self.selected_list)
        return queryset

    def get_context_data(self, **kwargs):
        return super().get_context_data(selected_list=self.selected_list, **kwargs)


class NoteCreateView(OwnerFormMixin, SuccessMessageMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'form.html'
    success_url = reverse_lazy('notes:index')
    success_message = 'Note "%(title)s" added.'
    extra_context = {'title': 'New note', 'cancel_url': reverse_lazy('notes:index')}

    def get(self, request, *args, **kwargs):
        if not NoteList.objects.filter(owner=request.user).exists():
            messages.info(request, 'Create a note list first, then add notes to it.')
            return redirect('notes:list_create')
        return super().get(request, *args, **kwargs)

    def get_initial(self):
        # Coming from a filtered note list, preselect that list.
        initial = super().get_initial()
        list_id = self.request.GET.get('list', '')
        if list_id.isdigit():
            initial['note_list'] = list_id
        return initial


class NoteUpdateView(OwnerQuerysetMixin, OwnerFormMixin, SuccessMessageMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'form.html'
    success_url = reverse_lazy('notes:index')
    success_message = 'Note "%(title)s" saved.'
    extra_context = {'title': 'Edit note', 'cancel_url': reverse_lazy('notes:index')}


class NoteDeleteView(OwnerQuerysetMixin, SuccessMessageMixin, DeleteView):
    model = Note
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('notes:index')
    success_message = 'Note deleted.'
    extra_context = {'title': 'Delete note', 'cancel_url': reverse_lazy('notes:index')}


# Note lists


class NoteListIndexView(OwnerQuerysetMixin, ListView):
    model = NoteList
    paginate_by = 20
    template_name = 'notes/notelist_index.html'

    def get_queryset(self):
        return super().get_queryset().annotate(note_count=Count('notes')).order_by('name')


class NoteListCreateView(OwnerFormMixin, SuccessMessageMixin, CreateView):
    model = NoteList
    form_class = NoteListForm
    template_name = 'form.html'
    success_url = reverse_lazy('notes:list_index')
    success_message = 'List "%(name)s" created.'
    extra_context = {'title': 'New note list', 'cancel_url': reverse_lazy('notes:list_index')}


class NoteListUpdateView(OwnerQuerysetMixin, OwnerFormMixin, SuccessMessageMixin, UpdateView):
    model = NoteList
    form_class = NoteListForm
    template_name = 'form.html'
    success_url = reverse_lazy('notes:list_index')
    success_message = 'List "%(name)s" saved.'
    extra_context = {'title': 'Edit note list', 'cancel_url': reverse_lazy('notes:list_index')}


class NoteListDeleteView(OwnerQuerysetMixin, SuccessMessageMixin, DeleteView):
    model = NoteList
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('notes:list_index')
    success_message = 'List deleted.'
    extra_context = {'title': 'Delete note list', 'cancel_url': reverse_lazy('notes:list_index')}

    def get_context_data(self, **kwargs):
        count = self.object.notes.count()
        if count:
            kwargs['warning'] = f'Its {count} note{"s" if count != 1 else ""} will be deleted too.'
        return super().get_context_data(**kwargs)
