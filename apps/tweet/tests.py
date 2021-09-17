import time

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.tweet.models import Post

User = get_user_model()


class TweetCreateTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('foo', 'foo@example.com', 'testpassword')
        self.client.login(username='foo', password='testpassword')
        self.url = reverse('apps.users:tweet_create')
    
    def test_tweet_create_view_get(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'tweet/tweet_create.html')

    def test_tweet_create_success(self):
        post_response = self.client.post(self.url, {'title': 'test','content':'test'})
        self.assertRedirects(post_response, reverse('apps.users:profile', kwargs={'username': self.user.username}))
    
    def test_tweet_create_failure_by_empty_field(self):
        post_response = self.client.post(self.url, {'title': 'test','content':''})
        self.assertFormError(post_response, 'form', 'content', 'このフィールドは必須です。')


class TweetListTests(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user('foo1', 'foo1@example.com', 'testpassword')
        self.user2 = User.objects.create_user('foo2', 'foo2@example.com', 'testpassword')
        self.tweet1 = Post.objects.create(title='test1', content='test1', user=self.user1)
        time.sleep(0.3)
        self.tweet2 = Post.objects.create(title='test2', content='test2', user=self.user2)
        self.url = reverse('apps.users:home')
    
    def test_tweet_list_get(self):
        self.client.login(username='foo1', password='testpassword')
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'tweet/tweet_list.html')
        self.assertQuerysetEqual(
            response.context['post_list'],
            ['<Post: test2>', '<Post: test1>'], 
            ordered = True
        )
        self.assertContains(response, self.user1.username)
        self.assertContains(response, self.tweet1.title)
        self.assertContains(response, self.user2.username)
        self.assertContains(response, self.tweet2.title)


class TweetDetailTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('foo', 'foo@example.com', 'testpassword')
        self.client.login(username='foo', password='testpassword')
        self.tweet = Post.objects.create(title='test', content='test', user=self.user)
        self.url = reverse('apps.users:tweet_detail', kwargs={'pk':self.tweet.pk})

    def test_tweet_detail_view_get(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'tweet/tweet_detail.html')
        self.assertContains(response, self.user.username)
        self.assertContains(response, self.tweet.title)
        self.assertContains(response, self.tweet.content)
    

class TweetDeleteTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('foo', 'foo@example.com', 'testpassword')
        self.tweet = Post.objects.create(title='test', content='test', user=self.user)
        self.url = reverse('apps.users:tweet_delete', kwargs={'pk':self.tweet.pk})

    def test_tweet_delete_view_get(self):
        self.client.login(username='foo', password='testpassword')
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'tweet/tweet_delete.html')
    
    def test_tweet_delete_success(self):
        self.client.login(username='foo', password='testpassword')
        response = self.client.delete(self.url)
        self.assertRedirects(response, reverse('apps.users:profile', kwargs={'username': self.user.username}))
    
    def test_tweet_delete_failure_by_not_correct_user(self):
        self.user1 = User.objects.create_user('foo1', 'foo1@example.com', 'testpassword')
        self.client.login(username='foo1', password='testpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)
