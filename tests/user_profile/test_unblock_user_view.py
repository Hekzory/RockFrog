from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client


class UnblockUserViewTestCase(TestCase):
    def setUp(self):
        self.unblock_user = User.objects.create_user('unblock_tester', 'unblock_test@test.test', 'testpassword')
        self.unblock_user2 = User.objects.create_user('unblock_tester2', 'unblock_test2@test.test', 'testpassword')
        self.unblock_user3 = User.objects.create_user('unblock_tester3', 'unblock_test3@test.test', 'testpassword')
        self.unblock_client = Client()
        self.unblock_client2 = Client()
        self.unblock_client3 = Client()
        self.unblock_client.force_login(self.unblock_user)
        self.unblock_client2.force_login(self.unblock_user2)
        self.unblock_client3.force_login(self.unblock_user3)
        self.unblock_user2.profile.blacklist.add(self.unblock_user3)
        self.unblock_user2.profile.save()

    def test_if_user_is_unauthenticated(self):
        unauth_client = Client()
        response = unauth_client.post('/profile/unblock/')
        self.assertJSONEqual(response.content, {'status': 'NotAuthenticated'})

    def test_if_user_tries_to_unblock_himself(self):
        response = self.unblock_client.post('/profile/unblock/', {'user_id':  self.unblock_user.id})
        self.assertJSONEqual(response.content, {'status': 'ok'})
        self.assertEqual(self.unblock_user in self.unblock_user.profile.blacklist.all(), False)

    def test_if_user_tries_to_unblock_an_nonexistent_user(self):
        response = self.unblock_client.post('/profile/unblock/', {'user_id': '0'})
        self.assertJSONEqual(response.content, {'status': 'UserNotFound'})

    def test_if_user_id_is_not_a_number(self):
        response = self.unblock_client.post('/profile/unblock/', {'user_id': 'kek'})
        self.assertJSONEqual(response.content, {'status': 'User_id is not a number'})

    def test_if_user_tries_to_unblock_a_user_that_is_not_in_his_blacklist(self):
        response = self.unblock_client.post('/profile/unblock/', {'user_id': self.unblock_user2.id})
        self.assertJSONEqual(response.content, {'status': 'ok'})

    def test_for_normal_situation(self):
        response = self.unblock_client2.post('/profile/unblock/', {'user_id': self.unblock_user3.id})
        self.assertJSONEqual(response.content, {'status': 'ok'})
        self.assertEqual(self.unblock_user3 in self.unblock_user2.profile.blacklist.all(), False)


