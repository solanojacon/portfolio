from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Note, NoteList

User = get_user_model()


class NoteTestCase(TestCase):
    """Two users with one list and one note each; Bob is logged in."""

    def setUp(self):
        self.alice = User.objects.create_user('alice')
        self.bob = User.objects.create_user('bob')
        self.alice_list = NoteList.objects.create(name='Alice list', owner=self.alice)
        self.bob_list = NoteList.objects.create(name='Bob list', owner=self.bob)
        self.alice_note = Note.objects.create(title='Alice note', note_list=self.alice_list, content='private', owner=self.alice)
        self.bob_note = Note.objects.create(title='Bob note', note_list=self.bob_list, owner=self.bob)
        self.client.force_login(self.bob)


class LoginRequiredTests(TestCase):
    def test_every_page_requires_login(self):
        for name, args in [
            ('notes:index', []), ('notes:create', []), ('notes:update', [1]), ('notes:delete', [1]),
            ('notes:list_index', []), ('notes:list_create', []), ('notes:list_update', [1]), ('notes:list_delete', [1]),
        ]:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                self.assertRedirects(self.client.get(url), f"{reverse('login')}?next={url}")


class IsolationTests(NoteTestCase):
    def test_index_shows_only_own_notes(self):
        response = self.client.get(reverse('notes:index'))
        self.assertContains(response, 'Bob note')
        self.assertNotContains(response, 'Alice note')

    def test_cannot_open_or_change_another_users_note(self):
        url = reverse('notes:update', args=[self.alice_note.pk])
        self.assertEqual(self.client.get(url).status_code, 404)
        response = self.client.post(url, {'title': 'Taken', 'note_list': self.bob_list.pk, 'content': 'x'})
        self.assertEqual(response.status_code, 404)
        self.alice_note.refresh_from_db()
        self.assertEqual((self.alice_note.title, self.alice_note.owner, self.alice_note.content), ('Alice note', self.alice, 'private'))

    def test_cannot_delete_another_users_note_or_list(self):
        self.assertEqual(self.client.post(reverse('notes:delete', args=[self.alice_note.pk])).status_code, 404)
        self.assertEqual(self.client.post(reverse('notes:list_delete', args=[self.alice_list.pk])).status_code, 404)
        self.assertTrue(Note.objects.filter(pk=self.alice_note.pk).exists())

    def test_owner_comes_from_the_logged_in_user(self):
        self.client.post(reverse('notes:create'), {'title': 'Mine', 'note_list': self.bob_list.pk, 'owner': self.alice.pk})
        self.assertEqual(Note.objects.get(title='Mine').owner, self.bob)

    def test_cannot_put_a_note_in_another_users_list(self):
        response = self.client.post(reverse('notes:create'), {'title': 'Sneaky', 'note_list': self.alice_list.pk})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Note.objects.filter(title='Sneaky').exists())


class NoteCrudTests(NoteTestCase):
    def test_create_and_edit_note(self):
        response = self.client.post(reverse('notes:create'), {
            'title': 'Recipe', 'note_list': self.bob_list.pk, 'starred': 'on', 'content': 'Flour, eggs',
        })
        self.assertRedirects(response, reverse('notes:index'))
        note = Note.objects.get(title='Recipe')
        self.assertTrue(note.starred)
        self.client.post(reverse('notes:update', args=[note.pk]), {'title': 'Recipe', 'note_list': self.bob_list.pk, 'content': 'Flour'})
        note.refresh_from_db()
        self.assertEqual((note.content, note.starred), ('Flour', False))

    def test_delete_asks_for_confirmation_first(self):
        url = reverse('notes:delete', args=[self.bob_note.pk])
        self.assertEqual(self.client.get(url).status_code, 200)
        self.assertTrue(Note.objects.filter(pk=self.bob_note.pk).exists())
        self.client.post(url)
        self.assertFalse(Note.objects.filter(pk=self.bob_note.pk).exists())

    def test_new_user_is_asked_to_create_a_list_first(self):
        carol = User.objects.create_user('carol')
        self.client.force_login(carol)
        self.assertRedirects(self.client.get(reverse('notes:create')), reverse('notes:list_create'))
