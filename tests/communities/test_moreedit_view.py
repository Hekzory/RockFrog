from django.test import TestCase
from django.contrib.auth.models import User
from communities.models import *
from django.test import Client

class MoreditViewTestCase(TestCase):
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

    def test_public_case_1(self):
        self.admin_client.post('/groups/' + str(self.group.id) + '/edit/moreedit/', {'type': 'public'})
        self.group.refresh_from_db()
        self.assertEqual(not self.group.public, True)

    def test_public_case_2(self):
    	self.admin_client.post('/groups/' + str(self.group.id) + '/edit/moreedit/', {'type': 'public'})
    	self.admin_client.post('/groups/' + str(self.group.id) + '/edit/moreedit/', {'type': 'public'})
    	self.assertEqual(self.group.public, True)

    def test_public_case_non_admin(self):
        self.user_client.post('/groups/' + str(self.group.id) + '/edit/moreedit/', {'type': 'public'})
        self.group.refresh_from_db()
        self.assertEqual(self.group.public, True)

    def test_public_case_deleting_subrequests(self):
    	self.admin_client.post('/groups/' + str(self.group.id) + '/edit/moreedit/', {'type': 'public'})
    	self.group.subrequests.add(self.user)
    	self.admin_client.post('/groups/' + str(self.group.id) + '/edit/moreedit/', {'type': 'public'})
    	self.assertEqual(not self.user in self.group.subrequests.all(), True)
	
    def test_delete_case(self):
    	self.group2 = Group(groupname='group2', admin=self.admin_user, pubdate = datetime.now())
    	self.group2.save()
    	groupid = self.group2.id
    	self.admin_client.post('/groups/' + str(self.group2.id) + '/edit/moreedit/', {'type': 'delete'})
    	self.assertEqual(not Group.objects.filter(id=groupid).exists(), True)

    def test_allowsub_case(self):
    	self.group.subrequests.add(self.user)
    	self.admin_client.post('/groups/' + str(self.group.id) + '/edit/moreedit/', {'type': 'allowsub', 'userid': self.user.id})
    	self.assertEqual(not self.user in self.group.subrequests.all() and self.user in self.group.subscribers.all(), True)

    def test_rejectsub_case(self):
    	self.group.subrequests.add(self.user)
    	self.admin_client.post('/groups/' + str(self.group.id) + '/edit/moreedit/', {'type': 'rejectsub', 'userid': self.user.id})
    	self.assertEqual(not self.user in self.group.subrequests.all() and not self.user in self.group.subscribers.all(), True)  

    def test_allowarticles_case(self):
        self.admin_client.post('/groups/' + str(self.group.id) + '/edit/moreedit/', {'type': 'allowarticles', 'data': 3})
        self.group.refresh_from_db()
        self.assertEqual(self.group.allowarticles == 3, True)    	   		

    def test_deletegroupimage_case(self):
    	self.group.image = '123'
    	self.group.save()
    	self.admin_client.post('/groups/' + str(self.group.id) + '/edit/moreedit/', {'type': 'deletegroupimage'})
    	self.group.refresh_from_db()
    	self.assertEqual(self.group.image == 'False', True)

    def test_checkslug_case(self):
    	self.admin_client.post('/groups/' + str(self.group.id) + '/edit/moreedit/', {'type': 'checkslug', 'slug': 'lol'})
    	self.group.refresh_from_db()
    	self.assertEqual(self.group.slug == 'lol', True)  

    def test_checkslug_case_2(self):
    	self.admin_client.post('/groups/' + str(self.group.id) + '/edit/moreedit/', {'type': 'checkslug', 'slug': '1lol'})
    	self.group.refresh_from_db()
    	self.assertEqual(self.group.slug == str(self.group.id), True)    

    def test_checkslug_case_3(self):
    	self.group2 = Group(groupname='group', admin=self.admin_user, pubdate = datetime.now()) 
    	self.group2.slug = str('slugw')
    	self.group2.save()
    	self.admin_client.post('/groups/' + str(self.group.id) + '/edit/moreedit/', {'type': 'checkslug', 'slug': 'slugw'})
    	self.group.refresh_from_db()
    	self.assertEqual(self.group.slug == str(self.group.id), True) 

    def test_checkslug_case_4(self):
    	self.admin_client.post('/groups/' + str(self.group.id) + '/edit/moreedit/', {'type': 'checkslug', 'slug': ''})
    	self.group.refresh_from_db()
    	self.assertEqual(self.group.slug == str(self.group.id), True) 

    def test_checkslug_case_5(self):
    	self.admin_client.post('/groups/' + str(self.group.id) + '/edit/moreedit/', {'type': 'checkslug', 'slug': 'a' * 100})
    	self.group.refresh_from_db()
    	self.assertEqual(self.group.slug == str(self.group.id), True) 

    def test_checkslug_case_6(self):
    	self.admin_client.post('/groups/' + str(self.group.id) + '/edit/moreedit/', {'type': 'checkslug', 'slug': 'AbrACaDabrA'})
    	self.group.refresh_from_db()
    	self.assertEqual(self.group.slug == 'abracadabra', True)

    def test_checkslug_case_7(self):
    	self.admin_client.post('/groups/' + str(self.group.id) + '/edit/moreedit/', {'type': 'checkslug', 'slug': 'AbrA CaDabrA'})
    	self.group.refresh_from_db()
    	self.assertEqual(self.group.slug == str(self.group.id), True)  	       	

    def test_editname_case(self):
    	self.admin_client.post('/groups/' + str(self.group.id) + '/edit/moreedit/', {'type': 'editname', 'data': 'groupkek'})
    	self.group.refresh_from_db()
    	self.assertEqual(self.group.groupname == 'groupkek', True) 

    def test_editname_case_2(self):
    	self.admin_client.post('/groups/' + str(self.group.id) + '/edit/moreedit/', {'type': 'editname', 'data': ''})
    	self.group.refresh_from_db()
    	self.assertEqual(self.group.groupname == 'group', True)

    def test_editname_case_3(self):
    	self.admin_client.post('/groups/' + str(self.group.id) + '/edit/moreedit/', {'type': 'editname', 'data': 'a' * 1000})
    	self.group.refresh_from_db()
    	self.assertEqual(self.group.groupname == 'group', True) 

    def test_editdescription_case(self):
    	self.admin_client.post('/groups/' + str(self.group.id) + '/edit/moreedit/', {'type': 'editdescription', 'data': 'description'})
    	self.group.refresh_from_db()
    	self.assertEqual(self.group.description == 'description', True)

    def test_editdescription_case_2(self):
    	self.admin_client.post('/groups/' + str(self.group.id) + '/edit/moreedit/', {'type': 'editdescription', 'data': 'a' * 5000})
    	self.group.refresh_from_db()
    	self.assertEqual(self.group.description == '', True) 