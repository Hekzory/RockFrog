from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from django.contrib import auth

class LoginViewTestCase(TestCase):
    def setUp(self):
        self.first_user = User.objects.create_user('tester', 'tester@test.com', 'testpassword')
        self.first_client = Client()
        self.first_client.force_login(self.first_user)
        self.second_user = User.objects.create_user('tester2', 'tester2@test.com', 'testpassword')
        self.second_client = Client()
        self.second_client.force_login(self.second_user)
        self.unauthorized_client = Client()

    def test_if_redirect_for_already_authorized_get(self):
        response = self.first_client.get('/auth/login/')
        self.assertEqual(response.status_code, 302)

    def test_if_redirect_for_already_authorized_post(self):
        response = self.first_client.get('/auth/login/')
        self.assertEqual(response.status_code, 302)

    def test_if_unauthorized_dont_get_redirected(self):
        response = self.unauthorized_client.get('/auth/login/')
        self.assertEqual(response.status_code, 200)

    def test_if_unauthorized_get_right_template(self):
        response = self.unauthorized_client.get('/auth/login/')
        self.assertTemplateUsed(response, 'authpages/login.html')

    def test_if_unauthorized_can_authorize(self):
        third_user = User.objects.create_user('tester3', 'tester3@test.com', 'testpassword')
        unauthorized_client_temp = Client()
        unauthorized_client_temp.post('/auth/login/', {'login': 'tester3', 'password' : 'testpassword'})
        user = auth.get_user(unauthorized_client_temp)
        self.assertEqual(user.is_authenticated, True)

    def test_if_unauthorized_cant_authorize_with_wrong_password(self):
        fourth_user = User.objects.create_user('tester4', 'tester3@test.com', 'testpassword2')
        unauthorized_client_temp = Client()
        unauthorized_client_temp.post('/auth/login/', {'login': 'tester4', 'password' : 'testpassword'})
        user = auth.get_user(unauthorized_client_temp)
        self.assertEqual(user.is_authenticated, False)

    def test_if_unauthorized_cant_authorize_to_unexistent_user(self):
        unauthorized_client_temp = Client()
        response = unauthorized_client_temp.post('/auth/login/', {'login': 'tester4423234', 'password' : 'testpassword'})
        user = auth.get_user(unauthorized_client_temp)
        self.assertEqual(user.is_authenticated, False)
        self.assertEqual(response.status_code, 200)

    def test_if_unsuccessful_login_have_right_response_code_and_template(self):
        unauthorized_client_temp = Client()
        response = unauthorized_client_temp.post('/auth/login/', {'login': 'tester4423234', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "authpages/login.html")