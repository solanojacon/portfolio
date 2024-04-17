from django.urls import path
from . import views
from .views import NoteList, NoteCreate, NoteUpdate

app_name = 'notes'

urlpatterns = [
    path('notes/test/', views.test, name='test'),
    path('notes/', NoteList.as_view(), name='notes'),
    path('notes/add/', NoteCreate.as_view(), name='add_note'),
    path('notes/edit/<int:pk>', NoteUpdate.as_view(), name='edit_note'),
    path('notes/delete/<int:pk>', views.delete_note, name='delete_note'),
    path('notes/lists/', views.lists, name='lists'),
    path('notes/lists/add/', views.add_list, name='add_list'),
    path('notes/lists/edit/<int:pk>', views.edit_list, name='edit_list'),
    path('notes/lists/delete/<int:pk>', views.delete_list, name='delete_list'),
]
