from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from datetime import datetime, date
from UserProfile.forms import *


class EditProfileViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('tester', 'test@test.test', 'testpassword')
        self.user.profile.about = 'kek'
        self.user.profile.birth_date = date(2002, 5, 17)
        self.user.profile.city = 'Moscow'
        self.user.profile.phone = '+78005553535'
        self.user.profile.interests = 'meme'
        self.client = Client()
        self.client.force_login(self.user)

    def test_get_if_unauthenticated(self):
        unauth_client = Client()
        response = unauth_client.get('/profile/edit/')
        self.assertEqual(response.status_code, 302)

    def test_get_template(self):
        response = self.client.get('/profile/edit/')
        self.assertTemplateUsed(response, 'UserProfile/editprofile.html')

    def test_get_form(self):
        response = self.client.get('/profile/edit/')
        form = response.context['form']
        self.assertIsInstance(form, ProfileForm)

    def test_get_html(self):
        response = self.client.get('/profile/edit/')
        self.assertContains(response, 'kek')
        self.assertContains(response, '17')
        self.assertContains(response, '5')
        self.assertContains(response, '2002')
        self.assertContains(response, 'Moscow')
        self.assertContains(response, '+78005553535')
        self.assertContains(response, 'meme')

    def test_get_if_200_status_code_for_normal_situation(self):
        response = self.client.get('/profile/edit/')
        self.assertEqual(response.status_code, 200)

    def test_post_if_unauthenticated(self):
        unauth_client = Client()
        response = unauth_client.post('/profile/edit/')
        self.assertEqual(response.status_code, 302)

    def test_post_template(self):
        response = self.client.post('/profile/edit/')
        self.assertTemplateUsed(response, 'UserProfile/editprofile.html')

    def test_post_values_if_form_is_valid(self):
        self.client.post('/profile/edit/', {'phone': '+79104734689', 'email': 'kek@kek.kek',
                                                       'interests': 'meme2', 'about': 'kek2', 'city': 'Paris',
                                                       'birth_date_day': '26', 'birth_date_month': '9',
                                                       'birth_date_year': '2003'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.profile.phone, '+79104734689')
        self.assertEqual(self.user.profile.email, 'kek@kek.kek')
        self.assertEqual(self.user.profile.interests, 'meme2')
        self.assertEqual(self.user.profile.about, 'kek2')
        self.assertEqual(self.user.profile.city, 'Paris')
        self.assertEqual(self.user.profile.birth_date, date(2003, 9, 26))

    def test_post_form_after_changing_if_form_is_valid(self):
        response = self.client.post('/profile/edit/', {'phone': '+79104778689', 'email': 'kek2@kek.kek',
                                            'interests': 'meme3', 'about': 'kek3', 'city': 'Paris2',
                                            'birth_date_day': '25', 'birth_date_month': '10',
                                            'birth_date_year': '2001'})
        self.assertContains(response, '+79104778689')
        self.assertContains(response, 'kek2@kek.kek')
        self.assertContains(response, 'meme3')
        self.assertContains(response, 'kek3')
        self.assertContains(response, 'Paris2')
        self.assertContains(response, '25')
        self.assertContains(response, '10')
        self.assertContains(response, '2001')

# Потом здесь появятся проверки на валидацию



