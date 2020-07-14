from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client


class EditPrivacyViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('tester', 'test@test.test', 'testpassword')
        self.user2 = User.objects.create_user('tester2', 'test2@test.test', 'testpassword')
        self.user3 = User.objects.create_user('tester3', 'test3@test.test', 'testpassword')
        self.user.profile.privacysettings.allow_to_view_for_unreg = True
        self.user2.profile.privacysettings.allow_to_view_for_unreg = False
        self.user3.profile.privacysettings.allow_to_view_for_unreg = False
        self.user.profile.save()
        self.user2.profile.save()
        self.user3.profile.save()
        self.client = Client()
        self.client2 = Client()
        self.client3 = Client()
        self.client.force_login(self.user)
        self.client2.force_login(self.user2)
        self.client3.force_login(self.user3)
        self.unauth_client = Client()

    def test_get_if_user_is_unauthenticated(self):
        response = self.unauth_client.get('/profile/edit_privacy/')
        self.assertEqual(response.status_code, 302)

    def test_post_if_user_is_unauthenticated(self):
        response = self.unauth_client.post('/profile/edit_privacy/')
        self.assertEqual(response.status_code, 302)

    def test_get_template_and_code_for_normal_situation(self):
        response = self.client.get('/profile/edit_privacy/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'UserProfile/edit_privacy.html')

    def test_post_changing_allowed_to_view_from_true_to_false(self):
        self.assertEqual(self.user.profile.privacysettings.allow_to_view_for_unreg, True)
        self.client.post('/profile/edit_privacy/', {'allow_to_view_for_unreg': False})
        self.user.refresh_from_db()
        self.assertEqual(self.user.profile.privacysettings.allow_to_view_for_unreg, False)

    def test_post_changing_allowed_to_view_from_false_to_true(self):
        self.assertEqual(self.user2.profile.privacysettings.allow_to_view_for_unreg, False)
        self.client2.post('/profile/edit_privacy/', {'allow_to_view_for_unreg': True})
        self.user2.refresh_from_db()
        self.assertEqual(self.user2.profile.privacysettings.allow_to_view_for_unreg, True)

    def test_post_with_invalid_form(self):
        self.client3.post('/profile/edit_privacy/', {'allow_to_view_for_unreg': 'True'})
        self.assertEqual(self.user3.profile.privacysettings.allow_to_view_for_unreg, False)