from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from personal_messages.models import *

class DialogPageViewTestCase(TestCase):
    def setUp(self):
        self.first_user = User.objects.create_user('tester', 'tester@test.com', 'testpassword')
        self.first_client = Client()
        self.first_client.force_login(self.first_user)
        self.second_user = User.objects.create_user('tester2', 'tester2@test.com', 'testpassword')
        self.second_client = Client()
        self.second_client.force_login(self.second_user)

    def test_if_redirect_for_unauthorized(self):
        unauthorized_client = Client()
        response = unauthorized_client.get('/conversations')
        self.assertEqual(response.status_code, 301)

    def test_if_conversations_list_have_new_conversations(self):
        self.first_client.get('/conversations/user/2')
        try:
            conversation = self.first_user.conversationlist.conversations.get(user1=self.first_user)
        except Conversation.DoesNotExist:
            self.fail('Conversation was not created after visit')



