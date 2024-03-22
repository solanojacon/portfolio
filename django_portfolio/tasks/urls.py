from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import RedirectView
from . import views
from .views import TaskList, TaskCreate, TaskUpdate # , delete_subtask

app_name = 'tasks'

urlpatterns = [
    # path('', views.index, name='index'),
    path('', RedirectView.as_view(url='tasks/', permanent=True)),
    path('register/', views.register, name='register'),
    path('tasks/test/', views.test, name='test'),
    path('tasks/', TaskList.as_view(), name='tasks'),
    path('tasks/add/', TaskCreate.as_view(), name='add_task'),
    path('tasks/edit/<int:pk>', TaskUpdate.as_view(), name='edit_task'),
    # path('tasks/subtasks/delete/<int:pk>/', delete_subtask, name='delete_subtask'),
    path('tasks/delete/<int:pk>', views.delete_task, name='delete_task'),
    path('tasks/lists/', views.lists, name='lists'),
    path('tasks/lists/add/', views.add_list, name='add_list'),
    path('tasks/lists/edit/<int:pk>', views.edit_list, name='edit_list'),
    path('tasks/lists/delete/<int:pk>', views.delete_list, name='delete_list'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # Enable the serving of static files during development
