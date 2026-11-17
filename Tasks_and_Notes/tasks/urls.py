from django.urls import path

from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.TaskIndexView.as_view(), name='index'),
    path('add/', views.TaskCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.TaskUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.TaskDeleteView.as_view(), name='delete'),
    path('lists/', views.TaskListIndexView.as_view(), name='list_index'),
    path('lists/add/', views.TaskListCreateView.as_view(), name='list_create'),
    path('lists/<int:pk>/edit/', views.TaskListUpdateView.as_view(), name='list_update'),
    path('lists/<int:pk>/delete/', views.TaskListDeleteView.as_view(), name='list_delete'),
]
