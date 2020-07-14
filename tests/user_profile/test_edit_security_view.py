from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from django.contrib.auth import authenticate


class EditSecurityViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('tester', 'test@test.test', 'testpassword')
        self.user2 = User.objects.create_user('tester2', 'test2@test.test', 'testpassword')
        self.client = Client()
        self.client2 = Client()
        self.client.force_login(self.user)
        self.client2.force_login(self.user2)
        self.unauth_client = Client()

    def test_get_if_user_is_unauthenticated(self):
        response = self.unauth_client.get('/profile/edit_security/')
        self.assertEqual(response.status_code, 302)

    def test_post_if_user_is_unauthenticated(self):
        response = self.unauth_client.post('/profile/edit_security/')
        self.assertEqual(response.status_code, 302)

    def test_get_template_and_code_for_normal_situation(self):
        response = self.client.get('/profile/edit_security/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'UserProfile/edit_security.html')

    def test_post_with_too_short_password(self):
        response = self.client.post('/profile/edit_security/', {'old_password': 'testpassword',
                                                                'new_password': '1', 'confirm_password': '1'})
        self.assertFormError(response, 'form', 'new_password', 'Минимальная длина пароля - 8.')
        check_user = authenticate(username=self.user.username, password='testpassword')
        self.assertNotEqual(check_user, None)

    def test_post_if_confirm_password_does_not_match(self):
        response = self.client.post('/profile/edit_security/', {'old_password': 'testpassword',
                                                                'new_password': 'testpassword2',
                                                                'confirm_password': 'testpassword3'})
        self.assertFormError(response, 'form', 'new_password', 'Пароли не совпадают.')
        check_user = authenticate(username=self.user.username, password='testpassword')
        self.assertNotEqual(check_user, None)

    def test_post_if_new_password_is_not_acceptable(self):
        response = self.client.post('/profile/edit_security/', {'old_password': 'testpassword',
                                                                'new_password': 'адхщбаадхщба',
                                                                'confirm_password': 'адхщбаадхщба'})
        self.assertFormError(response, 'form', 'new_password',
                             'В пароле могут присутствовать лишь английские буквы, цифры, дефис и знак подчёркивания')
        check_user = authenticate(username=self.user.username, password='testpassword')
        self.assertNotEqual(check_user, None)

    def test_post_if_new_password_is_the_same(self):
        response = self.client.post('/profile/edit_security/', {'old_password': 'testpassword',
                                                                'new_password': 'testpassword',
                                                                'confirm_password': 'testpassword'})
        self.assertFormError(response, 'form', 'new_password', 'Старый пароль совпадает с новым')
        check_user = authenticate(username=self.user.username, password='testpassword')
        self.assertNotEqual(check_user, None)

    def test_post_with_incorrect_old_password(self):
        response = self.client.post('/profile/edit_security/', {'old_password': 'burdaburda',
                                                                'new_password': 'testpassword1',
                                                                'confirm_password': 'testpassword1'})
        self.assertTemplateUsed(response, 'UserProfile/edit_security.html')
        self.assertContains(response, 'Текущий пароль указан неправильно.')
        check_user = authenticate(username=self.user.username, password='testpassword')
        self.assertNotEqual(check_user, None)

    def test_post_for_normal_situation(self):
        response = self.client.post('/profile/edit_security/', {'old_password': 'testpassword',
                                                                'new_password': 'testpassword1',
                                                                'confirm_password': 'testpassword1'})
        self.assertTemplateUsed(response, 'UserProfile/password_changed.html')
        check_user = authenticate(username=self.user.username, password='testpassword1')
        self.assertNotEqual(check_user, None)

    def test_post_with_invalid_form(self):
        response = self.client2.post('/profile/edit_security/', {'old_password': 'testpassword',
                                                                 'new_password': True,
                                                                 'confirm_password': True})
        self.assertTemplateUsed(response, 'UserProfile/edit_security.html')
        check_user = authenticate(username=self.user.username, password='testpassword')
        self.assertNotEqual(check_user, None)