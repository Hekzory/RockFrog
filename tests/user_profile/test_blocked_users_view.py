from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client


class BlockedUsersViewTestCase(TestCase):
    def setUp(self):
        self.unregistered_client = Client()
        self.user = User.objects.create_user('tester', 'tester@test.test', 'testpassword')
        self.client = Client()
        self.client.force_login(self.user)

    def test_if_not_authenticated(self):
        response = self.unregistered_client.get('/profile/blockedusers/')
        self.assertEqual(response.status_code, 302)

    def test_if_authenticated(self):
        response = self.client.get('/profile/blockedusers/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'UserProfile/blacklist.html')



