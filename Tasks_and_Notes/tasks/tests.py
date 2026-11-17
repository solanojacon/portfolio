from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Subtask, Task, TaskList

User = get_user_model()


def task_data(task_list, **overrides):
    """POST data for the task form, with an empty subtask formset."""
    data = {
        'title': 'Buy milk', 'task_list': task_list.pk, 'due_date': '', 'details': '',
        'subtasks-TOTAL_FORMS': 0, 'subtasks-INITIAL_FORMS': 0,
    }
    data.update(overrides)
    return data


class TaskTestCase(TestCase):
    """Two users with one list and one task each; Bob is logged in."""

    def setUp(self):
        self.alice = User.objects.create_user('alice')
        self.bob = User.objects.create_user('bob')
        self.alice_list = TaskList.objects.create(name='Alice list', owner=self.alice)
        self.bob_list = TaskList.objects.create(name='Bob list', owner=self.bob)
        self.alice_task = Task.objects.create(title='Alice task', task_list=self.alice_list, owner=self.alice)
        self.bob_task = Task.objects.create(title='Bob task', task_list=self.bob_list, owner=self.bob)
        self.client.force_login(self.bob)


class LoginRequiredTests(TestCase):
    def test_every_page_requires_login(self):
        for name, args in [
            ('tasks:index', []), ('tasks:create', []), ('tasks:update', [1]), ('tasks:delete', [1]),
            ('tasks:list_index', []), ('tasks:list_create', []), ('tasks:list_update', [1]), ('tasks:list_delete', [1]),
        ]:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                self.assertRedirects(self.client.get(url), f"{reverse('login')}?next={url}")


class IsolationTests(TaskTestCase):
    def test_index_shows_only_own_tasks(self):
        response = self.client.get(reverse('tasks:index'))
        self.assertContains(response, 'Bob task')
        self.assertNotContains(response, 'Alice task')

    def test_list_index_shows_only_own_lists(self):
        response = self.client.get(reverse('tasks:list_index'))
        self.assertContains(response, 'Bob list')
        self.assertNotContains(response, 'Alice list')

    def test_cannot_open_or_change_another_users_task(self):
        url = reverse('tasks:update', args=[self.alice_task.pk])
        self.assertEqual(self.client.get(url).status_code, 404)
        response = self.client.post(url, task_data(self.bob_list, title='Taken'))
        self.assertEqual(response.status_code, 404)
        self.alice_task.refresh_from_db()
        self.assertEqual((self.alice_task.title, self.alice_task.owner), ('Alice task', self.alice))

    def test_cannot_delete_another_users_task(self):
        response = self.client.post(reverse('tasks:delete', args=[self.alice_task.pk]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Task.objects.filter(pk=self.alice_task.pk).exists())

    def test_cannot_change_or_delete_another_users_list(self):
        update = self.client.post(reverse('tasks:list_update', args=[self.alice_list.pk]), {'name': 'X', 'color': '#000000'})
        delete = self.client.post(reverse('tasks:list_delete', args=[self.alice_list.pk]))
        self.assertEqual((update.status_code, delete.status_code), (404, 404))
        self.alice_list.refresh_from_db()
        self.assertEqual(self.alice_list.name, 'Alice list')

    def test_owner_comes_from_the_logged_in_user(self):
        self.client.post(reverse('tasks:list_create'), {'name': 'New', 'color': '#123456', 'owner': self.alice.pk})
        self.client.post(reverse('tasks:create'), task_data(self.bob_list, title='Mine', owner=self.alice.pk))
        self.assertEqual(TaskList.objects.get(name='New').owner, self.bob)
        self.assertEqual(Task.objects.get(title='Mine').owner, self.bob)

    def test_cannot_put_a_task_in_another_users_list(self):
        response = self.client.post(reverse('tasks:create'), task_data(self.alice_list, title='Sneaky'))
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'task_list', 'Select a valid choice. That choice is not one of the available choices.')
        self.assertFalse(Task.objects.filter(title='Sneaky').exists())

    def test_cannot_edit_subtasks_of_another_users_task(self):
        alice_subtask = Subtask.objects.create(title='Alice step', task=self.alice_task)
        self.client.post(reverse('tasks:update', args=[self.bob_task.pk]), task_data(
            self.bob_list, title='Bob task', **{
                'subtasks-TOTAL_FORMS': 1, 'subtasks-INITIAL_FORMS': 1,
                'subtasks-0-id': alice_subtask.pk, 'subtasks-0-title': 'Changed',
            },
        ))
        alice_subtask.refresh_from_db()
        self.assertEqual((alice_subtask.title, alice_subtask.task), ('Alice step', self.alice_task))


class TaskCrudTests(TaskTestCase):
    def test_create_task_with_subtasks(self):
        response = self.client.post(reverse('tasks:create'), task_data(
            self.bob_list, title='Trip', due_date='2030-01-15', **{
                'subtasks-TOTAL_FORMS': 3,
                'subtasks-0-title': 'Book flight', 'subtasks-0-completed': 'on',
                'subtasks-1-title': 'Pack',
                'subtasks-2-title': '',  # an empty row added and left blank is ignored
            },
        ))
        self.assertRedirects(response, reverse('tasks:index'))
        task = Task.objects.get(title='Trip')
        self.assertEqual(str(task.due_date), '2030-01-15')
        self.assertEqual([(s.title, s.completed) for s in task.subtasks.all()], [('Book flight', True), ('Pack', False)])

    def test_update_task_edits_and_deletes_subtasks(self):
        keep = Subtask.objects.create(title='Keep', task=self.bob_task)
        drop = Subtask.objects.create(title='Drop', task=self.bob_task)
        self.client.post(reverse('tasks:update', args=[self.bob_task.pk]), task_data(
            self.bob_list, title='Bob task', **{
                'subtasks-TOTAL_FORMS': 2, 'subtasks-INITIAL_FORMS': 2,
                'subtasks-0-id': keep.pk, 'subtasks-0-title': 'Keep', 'subtasks-0-completed': 'on',
                'subtasks-1-id': drop.pk, 'subtasks-1-title': 'Drop', 'subtasks-1-DELETE': 'on',
            },
        ))
        self.assertEqual(list(self.bob_task.subtasks.values_list('title', 'completed')), [('Keep', True)])

    def test_invalid_subtask_keeps_everything_unsaved(self):
        response = self.client.post(reverse('tasks:create'), task_data(
            self.bob_list, title='Half', **{'subtasks-TOTAL_FORMS': 1, 'subtasks-0-title': 'x' * 101},
        ))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(title='Half').exists())

    def test_delete_asks_for_confirmation_first(self):
        url = reverse('tasks:delete', args=[self.bob_task.pk])
        response = self.client.get(url)
        self.assertContains(response, "This can't be undone")
        self.assertTrue(Task.objects.filter(pk=self.bob_task.pk).exists())
        self.assertRedirects(self.client.post(url), reverse('tasks:index'))
        self.assertFalse(Task.objects.filter(pk=self.bob_task.pk).exists())

    def test_deleting_a_list_warns_and_deletes_its_tasks(self):
        url = reverse('tasks:list_delete', args=[self.bob_list.pk])
        self.assertContains(self.client.get(url), 'Its 1 task will be deleted too.')
        self.client.post(url)
        self.assertFalse(Task.objects.filter(pk=self.bob_task.pk).exists())

    def test_new_user_is_asked_to_create_a_list_first(self):
        carol = User.objects.create_user('carol')
        self.client.force_login(carol)
        self.assertRedirects(self.client.get(reverse('tasks:create')), reverse('tasks:list_create'))

    def test_filter_by_list(self):
        other = TaskList.objects.create(name='Other', owner=self.bob)
        Task.objects.create(title='Other task', task_list=other, owner=self.bob)
        response = self.client.get(reverse('tasks:index'), {'list': other.pk})
        self.assertContains(response, 'Other task')
        self.assertNotContains(response, 'Bob task')
        # Another user's list id is ignored, not used as a filter.
        response = self.client.get(reverse('tasks:index'), {'list': self.alice_list.pk})
        self.assertContains(response, 'Bob task')
        self.assertNotContains(response, 'Alice task')

    def test_open_tasks_come_first_by_due_date(self):
        Task.objects.create(title='Done early', task_list=self.bob_list, owner=self.bob, completed=True, due_date='2030-01-01')
        Task.objects.create(title='Due later', task_list=self.bob_list, owner=self.bob, due_date='2030-03-01')
        Task.objects.create(title='Due sooner', task_list=self.bob_list, owner=self.bob, due_date='2030-02-01')
        titles = [task.title for task in self.client.get(reverse('tasks:index')).context['object_list']]
        self.assertEqual(titles, ['Due sooner', 'Due later', 'Bob task', 'Done early'])

    def test_list_color_must_be_hex(self):
        response = self.client.post(reverse('tasks:list_create'), {'name': 'Bad', 'color': 'red;x:y'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(TaskList.objects.filter(name='Bad').exists())


class OverdueTests(TestCase):
    def test_is_overdue(self):
        today = timezone.localdate()
        self.assertTrue(Task(due_date=today - timedelta(days=1)).is_overdue)
        self.assertFalse(Task(due_date=today).is_overdue)
        self.assertFalse(Task(due_date=today - timedelta(days=1), completed=True).is_overdue)
        self.assertFalse(Task(due_date=None).is_overdue)
