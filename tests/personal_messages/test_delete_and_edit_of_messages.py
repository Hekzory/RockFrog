from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from personal_messages.models import *
from datetime import datetime, timedelta

class MessageEditAndDeleteTestCase(TestCase):
    def setUp(self):
        self.first_user = User.objects.create_user('tester', 'tester@test.com', 'testpassword')
        self.first_client = Client()
        self.first_client.force_login(self.first_user)
        self.second_user = User.objects.create_user('tester2', 'tester2@test.com', 'testpassword')
        self.second_client = Client()
        self.second_client.force_login(self.second_user)

    def test_if_unauthorized_cant_access_delete_func(self):
        message1 = ConversationMessage.objects.create(user=self.first_user, text="1", date_time=datetime.now())
        unauthorized_client = Client()
        response = unauthorized_client.post('/conversations/delete_message', {'message_id': message1.id})
        self.assertEqual(response.status_code, 302)
        message1.delete()

    def test_if_can_delete_own_message(self):
        message1 = ConversationMessage.objects.create(user=self.first_user, text="1", date_time=datetime.now())
        message1_id = message1.id
        self.first_client.post('/conversations/delete_message', {'message_id': message1.id})
        self.assertEqual(ConversationMessage.objects.filter(id=message1_id).exists(), False)

    def test_if_cant_delete_other_user_message(self):
        message1 = ConversationMessage.objects.create(user=self.first_user, text="1", date_time=datetime.now())
        message1_id = message1.id
        self.second_client.post('/conversations/delete_message', {'message_id': message1.id})
        self.assertEqual(ConversationMessage.objects.filter(id=message1_id).exists(), True)
        message1.delete()

    def test_if_cant_delete_too_old_messages(self):
        message1 = ConversationMessage.objects.create(user=self.first_user, text="1", date_time=datetime.now()-timedelta(hours=25))
        message1_id = message1.id
        self.first_client.post('/conversations/delete_message', {'message_id': message1.id})
        self.assertEqual(ConversationMessage.objects.filter(id=message1_id).exists(), True)
        message1.delete()

    def test_if_unauthorized_cant_access_edit_func(self):
        message1 = ConversationMessage.objects.create(user=self.first_user, text="1", date_time=datetime.now())
        unauthorized_client = Client()
        response = unauthorized_client.post('/conversations/edit_message', {'message_id': message1.id, 'message': '2'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ConversationMessage.objects.get(id=message1.id).text, '1')
        message1.delete()

    def test_if_can_edit_own_messages(self):
        message1 = ConversationMessage.objects.create(user=self.first_user, text="1", date_time=datetime.now())
        self.first_client.post('/conversations/edit_message', {'message_id': message1.id, 'message': '2'})
        self.assertEqual(ConversationMessage.objects.get(id=message1.id).text, '2')
        message1.delete()

    def test_if_cant_edit_others_messages(self):
        message1 = ConversationMessage.objects.create(user=self.first_user, text="1", date_time=datetime.now())
        self.second_client.post('/conversations/edit_message', {'message_id': message1.id, 'message': '2'})
        self.assertEqual(ConversationMessage.objects.get(id=message1.id).text, '1')
        message1.delete()

    def test_if_cant_too_old_messages(self):
        message1 = ConversationMessage.objects.create(user=self.first_user, text="1", date_time=datetime.now()-timedelta(hours=25))
        self.first_client.post('/conversations/edit_message', {'message_id': message1.id, 'message': '2'})
        self.assertEqual(ConversationMessage.objects.get(id=message1.id).text, '1')
        message1.delete()