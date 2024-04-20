from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

class NoteLists(models.Model):
    name = models.CharField(max_length=25, blank=False, null=False)
    color = models.CharField(max_length=7, default='#FFFFFF', blank=False, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    class Meta:
        ordering = ['owner', 'name']
    def get_absolute_url(self):
        return reverse('notes:edit_list', args=[str(self.id)])
    def __str__(self):
        return f'{self.name}'

class Notes(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    list = models.ForeignKey(NoteLists, on_delete=models.CASCADE, blank=False, null=False)
    starred = models.BooleanField(default=False)
    note = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    class Meta:
        ordering = ['owner', 'list', 'title']
    def get_absolute_url(self):
        return reverse('notes:edit_note', args=[str(self.id)])
    def __str__(self):
        return f'{self.owner} | {self.list} | {self.title}'
