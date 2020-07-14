from django.test import TestCase
from django.contrib.auth.models import User
from communities.models import *
from django.test import Client

class InformationViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('superduperuser', 'tester@test.com', 'testpassword')
        self.user_client = Client()
        self.user_client.force_login(self.user)

        self.admin_user = User.objects.create_user('groupadmin', 'tester@test.com', 'testpassword')
        self.admin_client = Client()
        self.admin_client.force_login(self.admin_user)

        self.group = Group(groupname='group', admin=self.admin_user, pubdate = datetime.now()) 
        self.group.slug = str(self.group.id) 
        self.group.save() 

    def test_for_200_status_code_for_normal_situation(self):
        response = self.user_client.get('/groups/' + self.group.slug + '/information/')
        self.assertEqual(response.status_code, 200)

    def test_for_template_for_normal_situation(self):
        response = self.user_client.get('/groups/' + self.group.slug + '/information/')
        self.assertTemplateUsed(response, 'communities/information.html')

    def test_for_admin_role_for_admin(self):
        response = self.admin_client.get('/groups/' + self.group.slug + '/information/')
        self.assertContains(response, '<div class="text2">Администратор</div>')

    def test_for_new_member(self):
        self.group.subscribers.add(self.user)
        self.group.save()
        response = self.admin_client.get('/groups/' + self.group.slug + '/information/')
        self.group.subscribers.remove(self.user)
        self.group.save()
        self.assertContains(response, 'superduperuser')       
