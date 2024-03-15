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
from .models import NoteLists, Notes
from .forms import ListForm, NoteForm

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

@login_required
def notes(request):
    superuser = request.user.is_superuser
    if superuser == True:
        notes_data = Notes.objects.all()
    else:
        notes_data = Notes.objects.filter(owner__exact=request.user.id)
    context = {
        'notes_data': notes_data,
        'superuser': superuser,
    }
    return render(request, 'notes.html', context) # render is a shortcut for HttpResponse

@login_required
def add_note(request):
    form = NoteForm(initial={'owner': request.user.id})
    if request.method=='POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('notes:notes')
    context = {'form': form}
    return render(request, 'add_note.html', context)

@login_required
def edit_note(request, pk):
    notes_data = get_object_or_404(Notes, pk=pk)
    form = NoteForm(instance=notes_data)
    if request.method=='POST':
        form = NoteForm(request.POST, instance=notes_data)
        if form.is_valid():
            form.save()
            return redirect('notes:notes')
    context = {'form': form}
    return render(request, 'edit_note.html', context)

@login_required
def delete_note(request, pk):
    notes_data = get_object_or_404(Notes, pk=pk)
    notes_data.delete()
    return redirect('notes:notes')

@login_required
def lists(request):
    superuser = request.user.is_superuser
    if superuser == True:
        lists_data = NoteLists.objects.all()
    else:
        lists_data = NoteLists.objects.filter(owner__exact=request.user.id)
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
            return redirect('notes:lists')
    context = {'form': form}
    return render(request, 'add_list.html', context)

@login_required
def edit_list(request, pk):
    lists_data = get_object_or_404(NoteLists, pk=pk)
    form = ListForm(instance=lists_data)
    if request.method=='POST':
        form = ListForm(request.POST, instance=lists_data)
        if form.is_valid():
            form.save()
            return redirect('notes:lists')
    context = {'form': form}
    return render(request, 'edit_list.html', context)

@login_required
def delete_list(request, pk):
    lists_data = get_object_or_404(NoteLists, pk=pk)
    lists_data.delete()
    return redirect('notes:lists')
