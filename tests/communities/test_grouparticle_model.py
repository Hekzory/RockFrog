from django.test import TestCase
from django.contrib.auth.models import User
from communities.models import *
from django.test import Client

class GroupArticleModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('superduperuser', 'tester@test.com', 'testpassword')
        self.subscriber = User.objects.create_user('subscriber', 'tester@test.com', 'testpassword')
        self.admin_user = User.objects.create_user('groupadmin', 'tester@test.com', 'testpassword')

        self.group = Group(groupname='group', admin=self.admin_user, pubdate = datetime.now()) 
        self.group.slug = str(self.group.id)    
        self.group.save() 
        self.group.subscribers.add(self.subscriber)  
        self.group.save()  

        self.article = GroupArticle(author=self.admin_user, group=self.group)
        self.article.save()

    def test_for_like(self):
        self.article.like(self.user)
        self.assertEqual(self.user in self.article.likes.all(), True)

    def test_for_like_not_allowed_article(self):
        self.article.allowed = False
        self.article.save()
        self.article.like(self.user)
        self.assertEqual(not self.user in self.article.likes.all(), True)

    def test_for_like_article_in_closed_group(self):
        self.group.public = False
        self.group.save()
        self.article.like(self.user)
        self.assertEqual(not self.user in self.article.likes.all(), True)

    def test_for_remove_like(self):
        self.article.like(self.user)
        self.article.removelike(self.user)
        self.assertEqual(not self.user in self.article.likes.all(), True)

    def test_for_remove_like_not_from_allowed_article(self):
        self.article.like(self.user)
        self.article.allowed = False
        self.article.save()        
        self.article.removelike(self.user)
        self.assertEqual(self.user in self.article.likes.all(), True)

    def test_for_remove_like_from_article_in_closed_group(self):
        self.article.like(self.user)
        self.group.public = False
        self.group.save()
        self.article.removelike(self.user)
        self.assertEqual(self.user in self.article.likes.all(), True)
