from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()
PASSWORD = 'a-long-test-password-1'


class RegisterTests(TestCase):
    def test_register_creates_user_and_logs_in(self):
        response = self.client.post(reverse('register'), {
            'username': 'carol', 'password1': PASSWORD, 'password2': PASSWORD,
        })
        self.assertRedirects(response, reverse('tasks:index'), fetch_redirect_response=False)
        self.assertTrue(User.objects.filter(username='carol').exists())
        self.assertEqual(int(self.client.session['_auth_user_id']), User.objects.get(username='carol').pk)

    def test_logged_in_user_is_sent_away_from_register(self):
        user = User.objects.create_user('alice', password=PASSWORD)
        self.client.force_login(user)
        response = self.client.get(reverse('register'))
        self.assertRedirects(response, reverse('tasks:index'), fetch_redirect_response=False)


class LoginLogoutTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('alice', password=PASSWORD)

    def test_login_ignores_external_next(self):
        response = self.client.post(reverse('login') + '?next=https://evil.example', {
            'username': 'alice', 'password': PASSWORD, 'next': 'https://evil.example',
        })
        self.assertRedirects(response, reverse('tasks:index'), fetch_redirect_response=False)

    def test_logout_requires_post(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(reverse('logout')).status_code, 405)
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('login'))
        self.assertNotIn('_auth_user_id', self.client.session)


class PasswordChangeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('alice', password=PASSWORD)
        self.client.force_login(self.user)

    def test_change_password_keeps_user_logged_in(self):
        new_password = 'another-long-password-2'
        response = self.client.post(reverse('password_change'), {
            'old_password': PASSWORD, 'new_password1': new_password, 'new_password2': new_password,
        })
        self.assertRedirects(response, reverse('tasks:index'), fetch_redirect_response=False)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(new_password))
        self.assertEqual(self.client.get(reverse('tasks:index')).status_code, 200)

    def test_wrong_old_password_is_rejected(self):
        response = self.client.post(reverse('password_change'), {
            'old_password': 'wrong', 'new_password1': 'x-long-password-3', 'new_password2': 'x-long-password-3',
        })
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(PASSWORD))
