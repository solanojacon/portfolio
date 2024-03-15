from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'notes'

urlpatterns = [
    # path('', views.index, name='index'),
    # path('', RedirectView.as_view(url='notes/', permanent=True)),
    path('notes/test/', views.test, name='test'),
    path('notes/', views.notes, name='notes'),
    path('notes/add/', views.add_note, name='add_note'),
    path('notes/edit/<int:pk>', views.edit_note, name='edit_note'),
    path('notes/delete/<int:pk>', views.delete_note, name='delete_note'),
    path('notes/lists/', views.lists, name='lists'),
    path('notes/lists/add/', views.add_list, name='add_list'),
    path('notes/lists/edit/<int:pk>', views.edit_list, name='edit_list'),
    path('notes/lists/delete/<int:pk>', views.delete_list, name='delete_list'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # Enable the serving of static files during development
