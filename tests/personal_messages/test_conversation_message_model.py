from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from personal_messages.models import ConversationMessage
import datetime
from django.utils import timezone

class DialogPageViewTestCase(TestCase):
    def setUp(self):
        self.first_user = User.objects.create_user('cmm_tester', 'tester@test.com', 'testpassword')

    def test_if_str_method_works_normally_under_32_symbols(self):
        message = ConversationMessage.objects.create(user=self.first_user, text="hello world!", date_time=datetime.datetime.now())
        self.assertEqual(str(message), "hello world!")

    def test_if_str_method_cuts_everything_above_32_symbols(self):
        message = ConversationMessage.objects.create(user=self.first_user, text="1234567890qwertyuiop[]asdfghjkl;'\zx", date_time=datetime.datetime.now())
        self.assertEqual(str(message), "1234567890qwertyuiop[]asdfghjkl;")

    def test_if_earlier_24_method_gives_true_for_new_messages(self):
        message = ConversationMessage.objects.create(user=self.first_user, text="1234567890qwertyuiop[]asdfghjkl;'\zx",
                                                     date_time=timezone.now())
        self.assertEqual(message.is_earlier_24(), True)

    def test_if_earlier_24_method_gives_false_for_old_messages(self):
        message = ConversationMessage.objects.create(user=self.first_user, text="1234567890qwertyuiop[]asdfghjkl;'\zx",
                                                     date_time=timezone.now() - datetime.timedelta(days=2))
        self.assertEqual(message.is_earlier_24(), False)