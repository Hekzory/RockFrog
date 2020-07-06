from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client


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
        response = unauthorized_client.get('/conversations/user/1')
        self.assertEqual(response.status_code, 302)

    def test_if_200_status_code_for_normal_situation(self):
        response = self.first_client.get('/conversations/user/'+str(self.second_user.id))
        self.assertEqual(response.status_code, 200)

    def test_if_redirect_from_own_id_conversation(self):
        response = self.first_client.get('/conversations/user/'+str(self.first_user.id))
        self.assertEqual(response.status_code, 302)

    def test_for_404_if_user_messaging_with_doesnt_exist(self):
        response = self.first_client.get('/conversations/user/52355454')
        self.assertEqual(response.status_code, 404)

    def test_access_if_noone_blacklisted(self):
        response = self.first_client.get('/conversations/user/'+str(self.second_user.id))
        self.assertEqual(response.context['is_viewer_blacklisted'], False)
        self.assertEqual(response.context['is_viewed_blacklisted'], False)

    def test_access_if_viewer_blacklisted_but_not_viewed(self):
        self.second_user.profile.blacklist.add(self.first_user)
        response = self.first_client.get('/conversations/user/'+str(self.second_user.id))
        self.assertEqual(response.context['is_viewed_blacklisted'], False)
        self.assertEqual(response.context['is_viewer_blacklisted'], True)
        self.second_user.profile.blacklist.remove(self.first_user)

    def test_access_if_viewed_blacklisted_but_not_viewer(self):
        self.first_user.profile.blacklist.add(self.second_user)
        response = self.first_client.get('/conversations/user/'+str(self.second_user.id))
        self.assertEqual(response.context['is_viewed_blacklisted'], True)
        self.assertEqual(response.context['is_viewer_blacklisted'], False)
        self.first_user.profile.blacklist.remove(self.second_user)

    def test_access_if_both_blacklisted(self):
        self.first_user.profile.blacklist.add(self.second_user)
        self.second_user.profile.blacklist.add(self.first_user)
        response = self.first_client.get('/conversations/user/'+str(self.second_user.id))
        self.assertEqual(response.context['is_viewed_blacklisted'], True)
        self.assertEqual(response.context['is_viewer_blacklisted'], True)
        self.first_user.profile.blacklist.remove(self.second_user)
        self.second_user.profile.blacklist.remove(self.first_user)


