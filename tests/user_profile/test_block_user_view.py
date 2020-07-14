from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client


class BlockUserViewTestCase(TestCase):
    def setUp(self):
        self.block_user = User.objects.create_user('block_tester', 'block_test@test.test', 'testpassword')
        self.block_user2 = User.objects.create_user('block_tester2', 'block_test2@test.test', 'testpassword')
        self.block_user3 = User.objects.create_user('block_tester3', 'block_test3@test.test', 'testpassword')
        self.block_client = Client()
        self.block_client2 = Client()
        self.block_client3 = Client()
        self.block_client.force_login(self.block_user)
        self.block_client2.force_login(self.block_user2)
        self.block_client3.force_login(self.block_user3)

    def test_if_user_is_unauthenticated(self):
        unauth_client = Client()
        response = unauth_client.post('/profile/block/')
        self.assertJSONEqual(response.content, {'status': 'NotAuthenticated'})

    def test_if_user_tries_to_block_himself(self):
        response = self.block_client.post('/profile/block/', {'user_id':  self.block_user.id})
        self.assertJSONEqual(response.content, {'status': 'CantBlockYourself'})
        self.assertEqual(self.block_user in self.block_user.profile.blacklist.all(), False)

    def test_if_user_tries_to_block_an_nonexistent_user(self):
        response = self.block_client.post('/profile/block/', {'user_id': '0'})
        self.assertJSONEqual(response.content, {'status': 'UserNotFound'})

    def test_if_user_id_is_not_a_number(self):
        response = self.block_client.post('/profile/block/', {'user_id': 'kek'})
        self.assertJSONEqual(response.content, {'status': 'User_id is not a number'})

    def test_if_user_is_already_in_blacklist(self):
        self.block_user.profile.blacklist.add(self.block_user2)
        self.block_user.profile.save()
        response = self.block_client.post('/profile/block/', {'user_id': self.block_user2.id})
        self.assertJSONEqual(response.content, {'status': 'ok'})
        self.assertEqual(self.block_user2 in self.block_user.profile.blacklist.all(), True)

    def test_for_normal_situation(self):
        response = self.block_client.post('/profile/block/', {'user_id': self.block_user3.id})
        self.assertJSONEqual(response.content, {'status': 'ok'})
        self.assertEqual(self.block_user3 in self.block_user.profile.blacklist.all(), True)
