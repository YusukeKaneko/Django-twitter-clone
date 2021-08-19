from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class SignUpTests(TestCase):

    def setUp(self):
        self.url = reverse('apps.registration:signup')
    
    def test_signup_view_get(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_signup_post_success(self):
        post_response = self.client.post(self.url, {'username': 'foo','email': 'foo@example.com','password1': 'testpassword','password2': 'testpassword',})
        self.assertRedirects(post_response, reverse('apps.registration:login'))
        self.assertTrue(User.objects.filter(username='foo').exists())

    def test_signup_post_failure_by_empty_field(self):
        post_response = self.client.post(self.url,{
        'username': '',
        'email': 'foo@example.com',
        'password1': 'testpassword',
        'password2': 'testpassword',
        })
        self.assertEquals(post_response.status_code, 200)
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
        self.assertEquals(post_response.status_code, 200)
        self.assertFormError(post_response, 'form', 'username', '同じユーザー名が既に登録済みです。')
    
    def test_signup_post_failure_by_defferent_password(self):
        post_response = self.client.post(self.url, {
        'username': 'foo',
        'email': 'foo@example.com',
        'password1': 'test',
        'password2': 'testpassword',
        })
        self.assertEquals(post_response.status_code, 200)
        self.assertEquals(User.objects.all().count(), 0)
        self.assertFormError(post_response, 'form', 'password2','確認用パスワードが一致しません。')
    
    def test_signup_post_failure_by_short_password(self):
        post_response = self.client.post(self.url, {
        'username': 'foo',
        'email': 'foo@example.com',
        'password1': 'bjki',
        'password2': 'bjki',
        })
        self.assertEquals(post_response.status_code, 200)
        self.assertEquals(User.objects.all().count(), 0)
        self.assertFormError(post_response, 'form', 'password2', 'このパスワードは短すぎます。最低 8 文字以上必要です。')
    
    def test_signup_post_failure_by_common_password(self):
        post_response = self.client.post(self.url, {
        'username': 'foo',
        'email': 'foo@example.com',
        'password1': '123456789',
        'password2': '123456789',
        })
        self.assertEquals(post_response.status_code, 200)
        self.assertEquals(User.objects.all().count(), 0)
        self.assertFormError(post_response, 'form', 'password2', 'このパスワードは一般的すぎます。') 


class LoginTests(TestCase):

    def setUp(self):
        User.objects.create_user('foo', 'foo@example.com', 'testpassword')
        self.url = reverse('apps.registration:login')
    
    def test_login_view_get(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
    
    def test_login_post_success(self):
        post_response = self.client.post(self.url, {
        'username': 'foo',
        'password': 'testpassword',
        })
        self.assertRedirects(post_response, reverse('apps.registration:index'))
    
    def test_login_post_failure_by_username(self):
        post_response = self.client.post(self.url, {
        'username': 'foo1',
        'password': 'testpassword',
        })
        self.assertEquals(post_response.status_code, 200)
        self.assertFormError(post_response, 'form', '__all__', '正しいユーザー名とパスワードを入力してください。どちらのフィールドも大文字と小文字は区別されます。') 
        
    
    def test_login_post_failure_by_password(self):
        post_response = self.client.post(self.url, {
        'username': 'foo',
        'password': 'test',
        })
        self.assertEquals(post_response.status_code, 200)
        self.assertFormError(post_response, 'form', '__all__', '正しいユーザー名とパスワードを入力してください。どちらのフィールドも大文字と小文字は区別されます。') 


class LogoutTests(TestCase):

    def setUp(self):
        User.objects.create_user('foo', 'foo@example.com', 'testpassword')
        self.client.login(username='foo', password='testpassword')
        self.url = reverse('apps.registration:logout')
    
    def test_logout(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('apps.registration:login'))

