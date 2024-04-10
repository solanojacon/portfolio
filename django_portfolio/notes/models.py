from colorfield.fields import ColorField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

class NoteLists(models.Model):
    COLOR_PALETTE = [
        ('#FFFFFF', 'White'),
        ('#C0C0C0', 'Silver'),
        ('#808080', 'Gray'),
        ('#000000', 'Black'),
        ('#FF0000', 'Red'),
        ('#800000', 'Maroon'),
        ('#FFFF00', 'Yellow'),
        ('#808000', 'Olive'),
        ('#00FF00', 'Lime'),
        ('#008000', 'Green'),
        ('#00FFFF', 'Aqua'),
        ('#008080', 'Teal'),
        ('#0000FF', 'Blue'),
        ('#000080', 'Navy'),
        ('#FF00FF', 'Fuchsia'),
        ('#800080', 'Purple'),
    ]
    name = models.CharField(max_length=25, blank=False, null=False)
    color = ColorField(samples=COLOR_PALETTE, default='#FFFFFF', blank=False, null=False)
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
