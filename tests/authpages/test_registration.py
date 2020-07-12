from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from django.contrib import auth


class RegistrationViewTestCase(TestCase):
    def setUp(self):
        self.first_user = User.objects.create_user('tester', 'tester@test.com', 'testpassword')
        self.first_client = Client()
        self.first_client.force_login(self.first_user)
        self.second_user = User.objects.create_user('tester2', 'tester2@test.com', 'testpassword')
        self.second_client = Client()
        self.second_client.force_login(self.second_user)
        self.unauthorized_client = Client()

    def test_if_redirect_for_already_authorized(self):
        response = self.first_client.get('/auth/register/')
        self.assertEqual(response.status_code, 302)

    def test_if_unauthorized_dont_get_redirected(self):
        response = self.unauthorized_client.get('/auth/register/')
        self.assertEqual(response.status_code, 200)

    def test_if_unauthorized_get_right_template(self):
        response = self.unauthorized_client.get('/auth/register/')
        self.assertTemplateUsed(response, 'authpages/register.html')

    def test_if_unauthorized_can_register(self):
        unauthorized_client_temp = Client()
        unauthorized_client_temp.post('/auth/register/', {'login': 'tester3', 'email': 'tester@gmail.com',  'password': 'testpassword', 'confirmpass': 'testpassword'})
        user = auth.get_user(unauthorized_client_temp)
        self.assertEqual(user.is_authenticated, True)

    def test_if_unauthorized_cant_register_with_existent_login(self):
        unauthorized_client_temp = Client()
        unauthorized_client_temp.post('/auth/register/', {'login': 'tester', 'email': 'tester3223@gmail.com',  'password': 'testpassword', 'confirmpass': 'testpassword'})
        user = auth.get_user(unauthorized_client_temp)
        self.assertEqual(user.is_authenticated, False)

    def test_if_unauthorized_cant_register_with_existent_email(self):
        unauthorized_client_temp = Client()
        unauthorized_client_temp.post('/auth/register/', {'login': 'tester6', 'email': 'tester@test.com',  'password': 'testpassword', 'confirmpass': 'testpassword'})
        user = auth.get_user(unauthorized_client_temp)
        self.assertEqual(user.is_authenticated, False)

    def test_if_unauthorized_cant_register_with_wrong_email(self):
        unauthorized_client_temp = Client()
        unauthorized_client_temp.post('/auth/register/', {'login': 'tester6', 'email': 'tester3345test.com',  'password': 'testpassword', 'confirmpass': 'testpassword'})
        user = auth.get_user(unauthorized_client_temp)
        self.assertEqual(user.is_authenticated, False)

    def test_if_unauthorized_cant_register_with_small_login(self):
        unauthorized_client_temp = Client()
        unauthorized_client_temp.post('/auth/register/', {'login': 't', 'email': 'tester3345@test.com',  'password': 'testpassword', 'confirmpass': 'testpassword'})
        user = auth.get_user(unauthorized_client_temp)
        self.assertEqual(user.is_authenticated, False)

    def test_if_unauthorized_cant_register_with_big_login(self):
        unauthorized_client_temp = Client()
        unauthorized_client_temp.post('/auth/register/', {'login': 't14313tnttntn52rggeregrgeg2352315235', 'email': 'tester3345@test.com',  'password': 'testpassword', 'confirmpass': 'testpassword'})
        user = auth.get_user(unauthorized_client_temp)
        self.assertEqual(user.is_authenticated, False)

    def test_if_unauthorized_cant_register_with_login_with_unallowed_symbols(self):
        unauthorized_client_temp = Client()
        unauthorized_client_temp.post('/auth/register/', {'login': 'abcd!123', 'email': 'tester3345@test.com',  'password': 'testpassword', 'confirmpass': 'testpassword'})
        user = auth.get_user(unauthorized_client_temp)
        self.assertEqual(user.is_authenticated, False)

    def test_if_unauthorized_cant_register_with_login_with_unallowed_symbols2(self):
        unauthorized_client_temp = Client()
        unauthorized_client_temp.post('/auth/register/', {'login': 'абвг123', 'email': 'tester3345@test.com',  'password': 'testpassword', 'confirmpass': 'testpassword'})
        user = auth.get_user(unauthorized_client_temp)
        self.assertEqual(user.is_authenticated, False)

    def test_if_unauthorized_cant_register_with_small_password(self):
        unauthorized_client_temp = Client()
        unauthorized_client_temp.post('/auth/register/', {'login': 'tester123', 'email': 'tester3345@test.com',  'password': 't', 'confirmpass': 't'})
        user = auth.get_user(unauthorized_client_temp)
        self.assertEqual(user.is_authenticated, False)

    def test_if_unauthorized_cant_register_with_big_password(self):
        unauthorized_client_temp = Client()
        unauthorized_client_temp.post('/auth/register/', {'login': 'tester123', 'email': 'tester3345@test.com',  'password': 'tttttttttttttttttttttttttttttttttttttttttttt', 'confirmpass': 'tttttttttttttttttttttttttttttttttttttttttttt'})
        user = auth.get_user(unauthorized_client_temp)
        self.assertEqual(user.is_authenticated, False)

    def test_if_unauthorized_cant_register_with_different_password_fields(self):
        unauthorized_client_temp = Client()
        unauthorized_client_temp.post('/auth/register/', {'login': 'tester123', 'email': 'tester3345@test.com',  'password': 'abcdek123456', 'confirmpass': 'abcdek12345'})
        user = auth.get_user(unauthorized_client_temp)
        self.assertEqual(user.is_authenticated, False)

    def test_if_unauthorized_cant_register_with_password_with_unallowed_symbols(self):
        unauthorized_client_temp = Client()
        unauthorized_client_temp.post('/auth/register/', {'login': 'tester123', 'email': 'tester3345@test.com',  'password': 'abcdekпро123456', 'confirmpass': 'abcdekпро123456'})
        user = auth.get_user(unauthorized_client_temp)
        self.assertEqual(user.is_authenticated, False)