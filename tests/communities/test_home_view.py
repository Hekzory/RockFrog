from django.test import TestCase
from django.contrib.auth.models import User
from communities.models import *
from django.test import Client

class HomeViewTestCase(TestCase):
	def setUp(self):
		self.user = User.objects.create_user('user', 'tester1@test.com', 'testpassword')
		self.auth_client = Client()
		self.auth_client.force_login(self.user)

		self.not_auth_client = Client()

	def test_if_200_status_code_for_normal_situation(self):
		response = self.auth_client.get('/groups/')
		self.assertEqual(response.status_code, 200)

	def test_if_word_for_auth_client(self):
		response = self.auth_client.get('/groups/')
		self.assertContains(response, 'заблокированы')

	def test_if_new_group_after_create(self):
		self.new_group = Group(groupname='AwoofAwoof', admin=self.user, pubdate = datetime.now())
		self.new_group.save()
		response = self.auth_client.get('/groups/')
		self.assertContains(response, self.new_group.groupname)