from django.conf import settings
from django.db import models
from django.urls import reverse

from core.forms import validate_hex_color


class NoteList(models.Model):
    name = models.CharField(max_length=25)
    color = models.CharField(max_length=7, default='#FFFFFF', validators=[validate_hex_color])
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='note_lists')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('notes:list_update', args=[self.pk])


class Note(models.Model):
    title = models.CharField(max_length=100)
    note_list = models.ForeignKey(NoteList, on_delete=models.CASCADE, related_name='notes', verbose_name='list')
    starred = models.BooleanField(default=False)
    content = models.TextField(blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notes')

    class Meta:
        ordering = ['-starred', 'title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('notes:update', args=[self.pk])
