from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from .models import NoteLists, Notes
from .forms import ListForm, NoteForm

@login_required
def test(request):
    template = loader.get_template('notes_test.html')
    context = {
        'fruits_data': ['Apple', 'Banana', 'Cherry'],
    }
    return HttpResponse(template.render(context, request))

@login_required
def lists(request):
    superuser = request.user.is_superuser
    if superuser == True:
        lists_data = NoteLists.objects.all()
    else:
        lists_data = NoteLists.objects.filter(owner__exact=request.user.id)
    paginator = Paginator(lists_data, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'lists_data': lists_data,
        'superuser': superuser,
        'page_obj': page_obj,
    }
    return render(request, 'notes_lists.html', context)

@login_required
def add_list(request):
    form = ListForm(initial={'owner': request.user.id})
    if request.method=='POST':
        form = ListForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('notes:lists')
    context = {'form': form}
    return render(request, 'notes_add_list.html', context)

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
    return render(request, 'notes_edit_list.html', context)

@login_required
def delete_list(request, pk):
    lists_data = get_object_or_404(NoteLists, pk=pk)
    lists_data.delete()
    return redirect('notes:lists')

@login_required
def notes(request):
    superuser = request.user.is_superuser
    if superuser == True:
        notes_data = Notes.objects.all()
    else:
        notes_data = Notes.objects.filter(owner__exact=request.user.id)
    paginator = Paginator(notes_data, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'notes_data': notes_data,
        'superuser': superuser,
        'page_obj': page_obj,
    }
    return render(request, 'notes_notes.html', context)

@login_required
def add_note(request):
    form = NoteForm(initial={'owner': request.user.id})
    if request.method=='POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('notes:notes')
    context = {'form': form}
    return render(request, 'notes_add_note.html', context)

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
    return render(request, 'notes_edit_note.html', context)

@login_required
def delete_note(request, pk):
    notes_data = get_object_or_404(Notes, pk=pk)
    notes_data.delete()
    return redirect('notes:notes')
