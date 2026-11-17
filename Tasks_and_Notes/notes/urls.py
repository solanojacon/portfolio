from django.urls import path

from . import views

app_name = 'notes'

urlpatterns = [
    path('', views.NoteIndexView.as_view(), name='index'),
    path('add/', views.NoteCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.NoteUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.NoteDeleteView.as_view(), name='delete'),
    path('lists/', views.NoteListIndexView.as_view(), name='list_index'),
    path('lists/add/', views.NoteListCreateView.as_view(), name='list_create'),
    path('lists/<int:pk>/edit/', views.NoteListUpdateView.as_view(), name='list_update'),
    path('lists/<int:pk>/delete/', views.NoteListDeleteView.as_view(), name='list_delete'),
]
