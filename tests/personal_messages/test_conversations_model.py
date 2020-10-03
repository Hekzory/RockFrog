from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from personal_messages.models import ConversationMessage, Conversation
import datetime
from django.utils import timezone

class DialogPageViewTestCase(TestCase):
    def setUp(self):
        self.first_user = User.objects.create_user('cm_tester', 'tester@test.com', 'testpassword')
        self.second_user = User.objects.create_user('cm_tester2', 'tester@test.com', 'testpassword')

    def test_if_update_interaction_method_works(self):
        conversation = Conversation.objects.create(user1=self.first_user, user2=self.second_user)
        first_time = conversation.last_interaction
        conversation.update_interaction()
        second_time = conversation.last_interaction
        self.assertEqual(first_time == second_time, False)
        self.assertEqual(first_time < second_time, True)
        conversation.delete()

    def test_if_update_user1_last_view_method_works(self):
        conversation = Conversation.objects.create(user1=self.first_user, user2=self.second_user)
        first_time = conversation.last_view_user1
        conversation.update_last_view_user1()
        second_time = conversation.last_view_user1
        self.assertEqual(first_time == second_time, False)
        self.assertEqual(first_time < second_time, True)
        conversation.delete()

    def test_if_update_user2_last_view_method_works(self):
        conversation = Conversation.objects.create(user1=self.first_user, user2=self.second_user)
        first_time = conversation.last_view_user2
        conversation.update_last_view_user2()
        second_time = conversation.last_view_user2
        self.assertEqual(first_time == second_time, False)
        self.assertEqual(first_time < second_time, True)
        conversation.delete()

    def test_if_str_method_works(self):
        conversation = Conversation.objects.create(user1=self.first_user, user2=self.second_user)
        self.assertEqual(str(conversation), "Conversation between "+str(self.first_user)+" and "+str(self.second_user))
        conversation.delete()

    def test_last_message_method_for_error_if_no_messages(self):
        conversation = Conversation.objects.create(user1=self.first_user, user2=self.second_user)
        result = conversation.get_last_message()
        self.assertEqual(result, "Возникла ошибка, пожалуйста, сообщите о ней администратору")
        conversation.delete()

    def test_last_message_author_method_for_error_if_no_messages(self):
        conversation = Conversation.objects.create(user1=self.first_user, user2=self.second_user)
        result = conversation.get_last_message_author()
        self.assertEqual(result, "Возникла ошибка, пожалуйста, сообщите о ней администратору")
        conversation.delete()

    def test_last_message_date_time_method_for_error_if_no_messages(self):
        conversation = Conversation.objects.create(user1=self.first_user, user2=self.second_user)
        result = conversation.get_last_message_date_time()
        self.assertEqual(result, None)
        conversation.delete()

    def test_get_last_message_method_if_gives_newest(self):
        conversation = Conversation.objects.create(user1=self.first_user, user2=self.second_user)
        message1 = ConversationMessage.objects.create(user=self.first_user, text='hi',
                                                      date_time=datetime.datetime.now())
        message2 = ConversationMessage.objects.create(user=self.first_user, text='hi',
                                                      date_time=datetime.datetime.now())
        conversation.messages.add(message1)
        conversation.messages.add(message2)
        result = conversation.get_last_message()
        self.assertEqual(result, message2.text)
        conversation.delete()

    def test_method_get_messages_sorted_by_date_if_gives_in_proper_order(self):
        conversation = Conversation.objects.create(user1=self.first_user, user2=self.second_user)
        message1 = ConversationMessage.objects.create(user=self.first_user, text='hi',
                                                      date_time=datetime.datetime.now())
        message2 = ConversationMessage.objects.create(user=self.first_user, text='hi',
                                                      date_time=datetime.datetime.now())
        conversation.messages.add(message1)
        conversation.messages.add(message2)
        result = conversation.get_messages_sorted_by_date()
        self.assertEqual(result[0].date_time <= result[1].date_time, True)
        conversation.delete()
