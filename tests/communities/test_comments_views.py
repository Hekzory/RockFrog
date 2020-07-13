from django.test import TestCase
from django.contrib.auth.models import User
from communities.models import *
from django.test import Client

class CommentsViewsTestCase(TestCase):
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

        self.article = GroupArticle(author=self.admin_user, group=self.group)
        self.article.save()

    def test_for_subsccriber_creating_comment(self):
        self.subscriber_client.post('/groups/' + str(self.group.id) + '/createcomment/' + str(self.article.id) + '/', {'text': 'CommentTextLolKek', 'reply': ''})
        self.assertEqual(self.article.comments.filter(text="CommentTextLolKek").exists(), True)  

    def test_for_deleting_comment(self):
        self.comment = GroupComment(author=self.subscriber, article=self.article, text="k")
        self.subscriber_client.post('/groups/deletecomment/' + str(self.comment.id) + '/')
        self.assertEqual(not self.article.comments.filter(text="k").exists(), True)

    def test_cant_delete_other_comment(self):
        self.comment = GroupComment(author=self.subscriber, article=self.article, text="k")
        self.user_client.post('/groups/deletecomment/' + str(self.comment.id) + '/')
        self.assertEqual(not self.article.comments.filter(text="k").exists(), True)

    def test_for_guest_creating_comment_in_closed_group(self):
        self.group.public = False
        self.group.save()
        self.user_client.post('/groups/' + str(self.group.id) + '/createcomment/' + str(self.article.id) + '/', {'text': 'CommentTextLolKek2', 'reply': ''})
        self.group.public = True
        self.group.save()
        self.assertEqual(not self.article.comments.filter(text="CommentTextLolKek2").exists(), True)

    def test_for_replying_comment(self):
        self.comment = GroupComment(author=self.subscriber, article=self.article, text="k")   
        self.comment.save()       
        self.subscriber_client.post('/groups/' + str(self.group.id) + '/createcomment/' + str(self.article.id) + '/', {'text': 'CommentTextLolKek3', 'reply': str(self.comment.id)})
        self.newcomment = self.article.comments.get(text="CommentTextLolKek3")
        self.assertEqual(self.newcomment.parent == self.comment and self.newcomment.replyto == self.comment.author, True)

    def test_for_replying_not_existing_comment(self):      
        self.subscriber_client.post('/groups/' + str(self.group.id) + '/createcomment/' + str(self.article.id) + '/', {'text': 'CommentTextLolKek4', 'reply': '1235'})
        self.newcomment = self.article.comments.get(text="CommentTextLolKek4")
        self.assertEqual(not self.newcomment.parent and not self.newcomment.replyto, True)

    def test_for_replying_replied_comment(self):
        self.comment = GroupComment(author=self.subscriber, article=self.article, text="k")   
        self.comment.save()    
        self.comment2 = GroupComment(author=self.subscriber, article=self.article, text="k", parent=self.comment, replyto=self.comment.author)   
        self.comment2.save()    
        self.subscriber_client.post('/groups/' + str(self.group.id) + '/createcomment/' + str(self.article.id) + '/', {'text': 'CommentTextLolKek5', 'reply': str(self.comment2.id)})
        self.newcomment = self.article.comments.get(text="CommentTextLolKek5")
        self.assertEqual(self.newcomment.parent == self.comment and self.newcomment.replyto == self.comment2.author, True)

    def test_for_deleting_replied_comment(self):
        self.comment = GroupComment(author=self.subscriber, article=self.article, text="k")   
        self.comment.save()    
        self.comment2 = GroupComment(author=self.subscriber, article=self.article, text="k1", parent=self.comment, replyto=self.comment.author)   
        self.comment2.save()    
        self.subscriber_client.post('/groups/deletecomment/' + str(self.comment.id) + '/')
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.is_deleted, True)

    def test_for_deleting_last_answer_under_deleted_comment(self):
        self.comment = GroupComment(author=self.subscriber, article=self.article, text="k")   
        self.comment.save()    
        self.comment2 = GroupComment(author=self.subscriber, article=self.article, text="k1", parent=self.comment, replyto=self.comment.author)   
        self.comment2.save()    
        self.subscriber_client.post('/groups/deletecomment/' + str(self.comment.id) + '/')
        self.comment.refresh_from_db()
        self.subscriber_client.post('/groups/deletecomment/' + str(self.comment2.id) + '/')
        self.assertEqual(not self.article.comments.filter(text="k").exists(), True)

    def test_edit_comment(self):
        self.comment = GroupComment(author=self.subscriber, article=self.article, text="k")   
        self.comment.save()   
        self.subscriber_client.post('/groups/editcomment/' + str(self.comment.id) + '/', {'text': 'aaa'})
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.text == "aaa", True)

    def test_cant_edit_other_comment(self):
        self.comment = GroupComment(author=self.admin_user, article=self.article, text="k")   
        self.comment.save()   
        self.subscriber_client.post('/groups/editcomment/' + str(self.comment.id) + '/', {'text': 'aaa'})
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.text != "aaa", True)

    def test_for_trying_to_create_comment_with_5000_symbols(self):
        self.subscriber_client.post('/groups/' + str(self.group.id) + '/createcomment/' + str(self.article.id) + '/', {'text': '0' * 5000, 'reply': ''})
        self.assertEqual(not self.article.comments.filter(text="CommentTextLolKek").exists(), True)         

    def test_for_trying_to_create_empty_comment(self):
        self.subscriber_client.post('/groups/' + str(self.group.id) + '/createcomment/' + str(self.article.id) + '/', {'text': '', 'reply': ''})
        self.assertEqual(not self.article.comments.filter(text="CommentTextLolKek").exists(), True)  

    def test_for_trying_to_edit_empty_comment(self):
        self.comment = GroupComment(author=self.subscriber, article=self.article, text="k")   
        self.comment.save()   
        self.subscriber_client.post('/groups/editcomment/' + str(self.comment.id) + '/', {'text': ''})
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.text == "k", True) 

    def test_for_trying_to_edit_comment_with_5000_symbols(self):
        self.comment = GroupComment(author=self.subscriber, article=self.article, text="k")   
        self.comment.save()   
        self.subscriber_client.post('/groups/editcomment/' + str(self.comment.id) + '/', {'text': '0' * 5000})
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.text == "k", True) 