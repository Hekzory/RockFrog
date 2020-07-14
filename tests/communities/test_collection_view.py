from django.test import TestCase
from django.contrib.auth.models import User
from communities.models import *
from django.test import Client

class CollectionViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('user', 'tester@test.com', 'testpassword')
        self.user_client = Client()
        self.user_client.force_login(self.user)

        self.admin_user = User.objects.create_user('groupadmin', 'tester@test.com', 'testpassword')
        self.admin_client = Client()
        self.admin_client.force_login(self.admin_user)

        self.group = Group(groupname='group', admin=self.admin_user, pubdate = datetime.now()) 
        self.group.slug = str(self.group.id) 
        self.group.save() 

    def test_for_200_status_code_for_normal_situation(self):
        response = self.user_client.get('/groups/' + self.group.slug + '/collection/')
        self.assertEqual(response.status_code, 200)

    def test_for_template_for_normal_situation(self):
        response = self.user_client.get('/groups/' + self.group.slug + '/collection/')
        self.assertTemplateUsed(response, 'communities/collection.html')
