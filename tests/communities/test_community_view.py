from django.test import TestCase
from django.contrib.auth.models import User
from communities.models import *
from django.test import Client

class CommunityViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('superduperuser', 'tester@test.com', 'testpassword')
        self.user_client = Client()
        self.user_client.force_login(self.user)

        self.subscriber = User.objects.create_user('subscriber', 'tester@test.com', 'testpassword')
        self.subscriber_client = Client()
        self.subscriber_client.force_login(self.subscriber)

        self.banned_user = User.objects.create_user('banned_user', 'tester@test.com', 'testpassword')
        self.banned_client = Client()
        self.banned_client.force_login(self.banned_user)

        self.admin_user = User.objects.create_user('groupadmin', 'tester@test.com', 'testpassword')
        self.admin_client = Client()
        self.admin_client.force_login(self.admin_user)

        self.group = Group(groupname='group', admin=self.admin_user, pubdate = datetime.now()) 
        self.group.slug = str(self.group.id)    
        self.group.save() 
        self.group.subscribers.add(self.subscriber)  
        self.group.save()  

    def test_if_200_status_code_for_normal_situation(self):
        response = self.user_client.get('/groups/' + self.group.slug + '/')
        self.assertEqual(response.status_code, 200)       

    def test_for_template_for_subscriber_in_closed_group(self):        
        self.group.public = False
        self.group.save()
        response = self.subscriber_client.get('/groups/' + self.group.slug + '/')
        self.group.public = True
        self.group.save()
        self.assertTemplateUsed(response, 'communities/community.html')

    def test_for_404_if_group_doesnt_exist(self):
        response = self.user_client.get('/groups/52/')
        self.assertEqual(response.status_code, 404)

    def test_for_template_if_group_closed(self):
        self.group.public = False
        self.group.save()
        response = self.user_client.get('/groups/' + self.group.slug + '/')
        self.group.public = True
        self.group.save()
        self.assertTemplateUsed(response, 'communities/closedgroup.html')

    def test_for_template_if_user_blacklisted(self):
        self.group.banned.add(self.banned_user)
        self.group.save()
        response = self.banned_client.get('/groups/' + self.group.slug + '/')
        self.assertTemplateUsed(response, 'communities/closedgroup.html')

    def test_for_subrequest(self):
        self.group.subrequests.add(self.user)
        self.group.public = False
        self.group.save()
        response = self.admin_client.get('/groups/' + self.group.slug + '/')
        self.group.subrequests.remove(self.user)
        self.group.public = True
        self.group.save()
        self.assertContains(response, 'superduperuser')    