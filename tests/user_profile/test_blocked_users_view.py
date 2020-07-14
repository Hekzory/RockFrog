from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client


class BlockedUsersViewTestCase(TestCase):
    def setUp(self):
        self.unregistered_client = Client()
        self.user = User.objects.create_user('tester', 'tester@test.test', 'testpassword')
        self.client = Client()
        self.client.force_login(self.user)
        self.user2 = User.objects.create_user('tester2', 'tester2@test.test', 'testpassword')
        self.client2 = Client()
        self.client2.force_login(self.user2)

    def test_if_not_authenticated(self):
        response = self.unregistered_client.get('/profile/blockedusers/')
        self.assertEqual(response.status_code, 302)

    def test_if_authenticated(self):
        response = self.client.get('/profile/blockedusers/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'UserProfile/blacklist.html')

    def test_if_user_was_added_to_blacklist(self):
        self.client.post('/profile/block/', {'user_id': self.user2.id})
        response = self.client.get('/profile/blockedusers/')
        self.assertContains(response, str(self.user2))

    def test_if_user_was_deleted_from_blacklist(self):
        self.client.post('/profile/unblock/', {'user_id': self.user2.id})
        response = self.client.get('/profile/blockedusers/')
        self.assertNotContains(response, str(self.user2))



