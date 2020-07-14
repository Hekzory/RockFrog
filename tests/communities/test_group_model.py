from django.test import TestCase
from django.contrib.auth.models import User
from communities.models import *
from django.test import Client

class GroupModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('superduperuser', 'tester@test.com', 'testpassword')
        self.admin_user = User.objects.create_user('groupadmin', 'tester@test.com', 'testpassword')

        self.group = Group(groupname='group', admin=self.admin_user, pubdate = datetime.now()) 
        self.group.slug = str(self.group.id) 
        self.group.save() 

    def test_for_subscribe_in_open_group(self):
        self.group.subscribe(self.user)
        if self.user in self.group.subscribers.all():
            self.group.subscribers.remove(self.user)
            self.group.save()
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_for_subscribe_in_closed_group(self):
        self.group.public = False
        self.group.save()
        self.group.subscribe(self.user)
        self.group.public = True
        self.group.save()
        if self.user in self.group.subscribers.all():
            self.group.subscribers.remove(self.user)
            self.group.save()
            self.assertTrue(False)
        else:
            self.assertTrue(True)

    def test_for_admin_trying_to_subscribe(self):
        self.group.subscribe(self.admin_user)
        if self.admin_user not in self.group.subscribers.all():            
            self.assertTrue(True)
        else:
            self.group.suscribers.remove(self.admin_user)
            self.group.save()
            self.assertTrue(False)

    def test_for_unsubscribe(self):
        self.group.subscribers.add(self.user)
        self.group.save()
        self.group.unsubscribe(self.user)
        if self.user in self.group.subscribers.all():
            self.group.subscribers.remove(self.user)
            self.group.save()
            self.assertTrue(False)
        else:
            self.assertTrue(True)

    def test_for_send_subrequest_in_closed_group(self):
        self.group.public = False
        self.group.save()
        self.group.send_subrequest(self.user)
        self.group.public = True
        self.group.save()
        if self.user in self.group.subrequests.all():
            self.group.subrequests.remove(self.user)
            self.group.save()
            self.assertTrue(True) 
        else:
            self.assertTrue(False)    

    def test_for_send_subrequest_in_open_group(self):
        self.group.send_subrequest(self.user)
        if self.user in self.group.subrequests.all():
            self.group.subrequests.remove(self.user)
            self.group.save()
            self.assertTrue(False) 
        else:
            self.assertTrue(True) 

    def test_for_admin_send_subrequest_in_closed_group(self):
        self.group.public = False
        self.group.save()
        self.group.send_subrequest(self.admin_user)
        self.group.public = True
        self.group.save()
        if self.admin_user in self.group.subrequests.all():
            self.group.subrequests.remove(self.admin_user)
            self.group.save()
            self.assertTrue(False) 
        else:
            self.assertTrue(True)    

    def test_for_cancel_subrequest(self):      
        self.group.public = False
        self.group.save()
        self.group.send_subrequest(self.user)
        self.group.cancel_subrequest(self.user)
        self.assertEqual(not self.user in self.group.subrequests.all(), True)     

    def test_for_cancel_non_existing_subrequest(self):      
        self.group.cancel_subrequest(self.user)
        self.assertEqual(not self.user in self.group.subrequests.all(), True)   


   
