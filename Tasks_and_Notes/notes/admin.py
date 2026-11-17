from django.contrib import admin

from .models import Note, NoteList


@admin.register(NoteList)
class NoteListAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'color']
    list_filter = ['owner']
    search_fields = ['name']


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'note_list', 'owner', 'starred']
    list_filter = ['starred', 'owner']
    search_fields = ['title', 'content']
