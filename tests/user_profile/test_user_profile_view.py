from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client


class UserProfileViewTestCase(TestCase):
    def setUp(self):
        self.first_user = User.objects.create_user('tester1', 'tester1@test.com', 'test1password')
        self.first_client = Client()
        self.first_client.force_login(self.first_user)
        self.second_user = User.objects.create_user('tester2', 'tester2@test.com', 'test2password')
        self.second_client = Client()
        self.second_client.force_login(self.second_user)

    def test_if_viewed_user_not_found(self):
        response = self.first_client.get('/profile/adhshba'+'/')
        self.assertEqual(response.status_code, 404)

    def test_if_user_tries_to_view_himself(self):
        response = self.first_client.get('/profile/' + str(self.first_user)+'/')
        self.assertEqual(response.status_code, 302)

    def test_if_200_status_code_for_normal_situation(self):
        response = self.first_client.get('/profile/' + str(self.second_user)+'/')
        self.assertEqual(response.status_code, 200)

    def test_if_authenticated_and_not_in_blacklist(self):
        response = self.first_client.get('/profile/' + str(self.second_user)+'/')
        self.assertTemplateUsed(response, 'UserProfile/userprofile.html')

    def test_if_authenticated_and_in_blacklist(self):
        self.second_user.profile.blacklist.add(self.first_user)
        response = self.first_client.get('/profile/' + str(self.second_user)+'/')
        self.assertTemplateUsed(response, 'UserProfile/blocked_forbidden.html')
        self.second_user.profile.blacklist.remove(self.first_user)

    def test_if_unregistered_and_allowed_to_view(self):
        unauthorized_client = Client()
        self.first_user.profile.privacysettings.allow_to_view_for_unreg = True
        self.first_user.profile.privacysettings.save()
        response = unauthorized_client.get('/profile/' + str(self.first_user)+'/')
        self.assertTemplateUsed(response, 'UserProfile/userprofile.html')

    def test_if_unregistered_and_not_allowed_to_view(self):
        unauthorized_client = Client()
        self.first_user.profile.privacysettings.allow_to_view_for_unreg = False
        self.first_user.profile.privacysettings.save()
        response = unauthorized_client.get('/profile/' + str(self.first_user)+'/')
        self.assertTemplateUsed(response, 'UserProfile/unregistered_forbidden.html')


