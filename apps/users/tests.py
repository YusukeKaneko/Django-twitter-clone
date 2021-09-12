from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from apps.tweet.models import Post
from apps.users.models import Connection

User = get_user_model()


class SignUpTests(TestCase):

    def setUp(self):
        self.url = reverse('apps.users:signup')
    
    def test_signup_view_get(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_signup_post_success(self):
        post_response = self.client.post(self.url, {'username': 'foo','email': 'foo@example.com','password1': 'testpassword','password2': 'testpassword',})
        self.assertRedirects(post_response, reverse('apps.users:login'))
        self.assertTrue(User.objects.filter(username='foo').exists())

    def test_signup_post_failure_by_empty_field(self):
        post_response = self.client.post(self.url,{
        'username': '',
        'email': 'foo@example.com',
        'password1': 'testpassword',
        'password2': 'testpassword',
        })
        self.assertEquals(User.objects.all().count(), 0)
        self.assertFormError(post_response, 'form', 'username', 'このフィールドは必須です。')
        
    def test_signup_post_failure_by_existed_username(self):
        User.objects.create_user('foo1', 'foo1@example.com', 'testpassword1')
        post_response = self.client.post(self.url, {
        'username': 'foo1',
        'email': 'foo1@example.com',
        'password1': 'testpassword1',
        'password2': 'testpassword1',
        })
        self.assertFormError(post_response, 'form', 'username', '同じユーザー名が既に登録済みです。')
    
    def test_signup_post_failure_by_defferent_password(self):
        post_response = self.client.post(self.url, {
        'username': 'foo',
        'email': 'foo@example.com',
        'password1': 'test',
        'password2': 'testpassword',
        })
        self.assertEquals(User.objects.all().count(), 0)
        self.assertFormError(post_response, 'form', 'password2','確認用パスワードが一致しません。')
    
    def test_signup_post_failure_by_short_password(self):
        post_response = self.client.post(self.url, {
        'username': 'foo',
        'email': 'foo@example.com',
        'password1': 'bjki',
        'password2': 'bjki',
        })
        self.assertEquals(User.objects.all().count(), 0)
        self.assertFormError(post_response, 'form', 'password2', 'このパスワードは短すぎます。最低 8 文字以上必要です。')
    
    def test_signup_post_failure_by_common_password(self):
        post_response = self.client.post(self.url, {
        'username': 'foo',
        'email': 'foo@example.com',
        'password1': '123456789',
        'password2': '123456789',
        })
        self.assertEquals(User.objects.all().count(), 0)
        self.assertFormError(post_response, 'form', 'password2', 'このパスワードは一般的すぎます。') 


class LoginTests(TestCase):

    def setUp(self):
        User.objects.create_user('foo', 'foo@example.com', 'testpassword')
        self.url = reverse('apps.users:login')
    
    def test_login_view_get(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
    
    def test_login_post_success(self):
        post_response = self.client.post(self.url, {
        'username': 'foo',
        'password': 'testpassword',
        })
        self.assertRedirects(post_response, reverse('apps.tweet:home'))
    
    def test_login_post_failure_by_username(self):
        post_response = self.client.post(self.url, {
        'username': 'foo1',
        'password': 'testpassword',
        })
        self.assertFormError(post_response, 'form', '__all__', '正しいユーザー名とパスワードを入力してください。どちらのフィールドも大文字と小文字は区別されます。') 
        
    
    def test_login_post_failure_by_password(self):
        post_response = self.client.post(self.url, {
        'username': 'foo',
        'password': 'test',
        })
        self.assertFormError(post_response, 'form', '__all__', '正しいユーザー名とパスワードを入力してください。どちらのフィールドも大文字と小文字は区別されます。') 


class LogoutTests(TestCase):

    def setUp(self):
        User.objects.create_user('foo', 'foo@example.com', 'testpassword')
        self.client.login(username='foo', password='testpassword')
        self.url = reverse('apps.users:logout')
    
    def test_logout(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('apps.users:login'))


class FollowTests(TestCase):
    
    def setUp(self):
        self.user1 = User.objects.create_user('foo1', 'foo1@example.com', 'testpassword')
        self.user2 = User.objects.create_user('foo2', 'foo2@example.com', 'testpassword')
        self.url1 = reverse('apps.users:follow_in_profile', kwargs={'pk':self.user1.pk})
        self.url2 = reverse('apps.users:follow_in_profile', kwargs={'pk':self.user2.pk})
    
    def test_follow_success(self):
        self.client.login(username='foo1', password='testpassword')
        response = self.client.get(self.url2)
        self.assertRedirects(response, reverse('apps.users:profile', kwargs={'username': self.user2.username}))
        following = Connection.objects.filter(user=self.user1).values_list('following')
        following_list = User.objects.filter(id__in=following)
        for following in following_list:
            self.assertEqual(following.username, 'foo2')
    
    def test_unfollow_success(self):
        self.client.login(username='foo1', password='testpassword')
        self.client.get(self.url2)
        self.client.get(self.url2)
        following = Connection.objects.filter(user=self.user1).values_list('following')
        following_list = User.objects.filter(id__in=following).count()
        self.assertEqual(following_list, 0)

    def test_follow_failure_by_common_user(self):
        self.client.login(username='foo1', password='testpassword')
        response = self.client.get(self.url1)
        self.assertRedirects(response, reverse('apps.users:profile', kwargs={'username': self.user1.username}))
        messages = list(get_messages(response.wsgi_request))
        message = str(messages[0])
        self.assertEqual(message, '自分をフォローすることはできません')
        following = Connection.objects.filter(user=self.user1).values_list('following')
        following_list = User.objects.filter(id__in=following).count()
        self.assertEqual(following_list, 0)


class FollowingAndFollowersListTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user('foo1', 'foo1@example.com', 'testpassword')
        self.user2 = User.objects.create_user('foo2', 'foo2@example.com', 'testpassword')
        self.client.login(username='foo1', password='testpassword')
        self.client.get(reverse('apps.users:follow_in_profile', kwargs={'pk':self.user2.pk}))
        self.client.login(username='foo2', password='testpassword')
        self.client.get(reverse('apps.users:follow_in_profile', kwargs={'pk':self.user1.pk}))
        self.url1 = reverse('apps.users:following_list', kwargs={'username':self.user1.username})
        self.url2 = reverse('apps.users:followers_list', kwargs={'username':self.user1.username})
    
    def test_following_list_get(self):
        self.client.login(username='foo1', password='testpassword')
        response = self.client.get(self.url1)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/following_list.html')
        self.assertQuerysetEqual(
            response.context['following_list'],
            ['<User: foo2>'], 
        )
        self.assertContains(response, self.user2.username)
    
    def test_followers_list_get(self):
        self.client.login(username='foo1', password='testpassword')
        response = self.client.get(self.url2)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/followers_list.html')
        self.assertQuerysetEqual(
            response.context['followers_list'],
            ['<Connection: foo2>'], 
        )
        self.assertContains(response, self.user2.username)


class UserProfileTest(TestCase):
        
    def setUp(self):
        self.user1 = User.objects.create_user('foo1', 'foo1@example.com', 'testpassword')
        self.user2 = User.objects.create_user('foo2', 'foo2@example.com', 'testpassword')
        self.client.login(username='foo1', password='testpassword')
        self.client.get(reverse('apps.users:follow_in_profile', kwargs={'pk':self.user2.pk}))
        self.client.login(username='foo2', password='testpassword')
        self.client.get(reverse('apps.users:follow_in_profile', kwargs={'pk':self.user1.pk}))
        self.tweet1 = Post.objects.create(title='test1', content='test1', user=self.user1)
        self.tweet2 = Post.objects.create(title='test2', content='test2', user=self.user2)
        self.url1 = reverse('apps.users:profile', kwargs={'username': self.user1.username})
        self.url2 = reverse('apps.users:profile', kwargs={'username': self.user2.username})

    def test_user1_profile_get(self):
        self.client.login(username='foo1', password='testpassword')
        response = self.client.get(self.url1)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertEqual(response.context['user_data'].username, 'foo1')
        self.assertContains(response, self.user1.username)
        self.assertQuerysetEqual(
            response.context['post_data'],
            ['<Post: test1>'],
            ordered = True
        )
        self.assertContains(response, self.tweet1.title)
        self.assertEqual(response.context['following_count'], 1)
        self.assertEqual(response.context['followers_count'], 1)
        request_user_following_list = response.context['request_user_following_list']
        for request_user_following in request_user_following_list:
            self.assertEqual(request_user_following.username, 'foo2')
    
    def test_user2_profile_get(self):
        self.client.login(username='foo1', password='testpassword')
        response = self.client.get(self.url2)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertEqual(response.context['user_data'].username, 'foo2')
        self.assertContains(response, self.user1.username)
        self.assertQuerysetEqual(
            response.context['post_data'],
            ['<Post: test2>'],
            ordered = True
        )
        self.assertContains(response, self.tweet2.title)
        self.assertEqual(response.context['following_count'], 1)
        self.assertEqual(response.context['followers_count'], 1)

