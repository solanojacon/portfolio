from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='tasks:index'), name='home'),
    path('accounts/', include('core.urls')),
    path('tasks/', include('tasks.urls')),
    path('notes/', include('notes.urls')),
    path('admin/', admin.site.urls),
]
