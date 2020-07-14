from django.test import TestCase
from django.contrib.auth.models import User
from communities.models import *
from django.test import Client

class EditViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('superduperuser', 'tester@test.com', 'testpassword')
        self.user_client = Client()
        self.user_client.force_login(self.user)

        self.admin_user = User.objects.create_user('groupadmin', 'tester@test.com', 'testpassword')
        self.admin_client = Client()
        self.admin_client.force_login(self.admin_user)

        self.group = Group(groupname='group', admin=self.admin_user, pubdate = datetime.now()) 
        self.group.save() 
        self.group.slug = str(self.group.id) 
        self.group.save() 

    def test_allowarticle_case(self):
        newarticle = GroupArticle(author=self.user, group=self.group, allowed=False)
        newarticle.save()
        self.admin_client.post('/groups/' + str(self.group.id) + '/moreedit/', {'type': 'allowarticle', 'data': newarticle.id})
        newarticle.refresh_from_db()
        self.assertEqual(newarticle.allowed, True)

    def test_deletearticle_case(self):
        newarticle = GroupArticle(author=self.user, group=self.group, allowed=False)
        newarticle.save()
        articleid = newarticle.id
        self.admin_client.post('/groups/' + str(self.group.id) + '/moreedit/', {'type': 'deletearticle', 'data': newarticle.id})
        self.assertEqual(not GroupArticle.objects.filter(id=articleid).exists(), True)