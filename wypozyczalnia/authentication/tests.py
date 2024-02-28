from django.test import TestCase, Client
from .models import CustomUser
from django.urls import reverse
from django.contrib.auth import get_user_model
from .views import create_user_activation_token

# Create your tests here.

class CustomUserModelTest(TestCase): 

    def test_create_multiple_users(self):
        for i in range(1000):
            user = CustomUser.objects.create(
                first_name=f"Test {i}",
                last_name=f"Test {i}",
                phone="123456789",
                adress="Street",
                city="City",
                postal_code="12345",
                email=f"test{i}@test.com",
                password="password"
            )
            self.assertIsNotNone(user)
            self.assertIsInstance(user, CustomUser)

class TokenTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpassword',
            first_name='test',
            is_active=False,
        )
        self.activation_token = create_user_activation_token(self.user)
    
    def test_create_token(self):
        token = create_user_activation_token(self.user)
        user2 = get_user_model().objects.create_user(
            email='test2@test.com',
            password='testpassword',
            first_name='test',
            is_active=False,
        )
        token2 = create_user_activation_token(user2)
        self.assertNotEqual(token, token2)
        self.assertEqual(self.activation_token, token)
    
    def test_activate(self):
        response = self.client.get(reverse('activate', args=[str(self.user.id), self.activation_token]))
        self.assertRedirects(response, reverse('home'))
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)
        messages_list = list(response.wsgi_request._messages)
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), "Aktywacja konta przebiegła pomyślnie. Możesz się teraz zalogować.")


class SignupTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_signup(self):
        response = self.client.post(reverse('signup'), {
            'email': 'test@test.com',
            'firstname': 'test',
            'lastname': 'test',
            'phone': '123456789',
            'city': 'test',
            'postal_code': '12345',
            'adress': 'test',
            'password1': 'testpassword',
            'password2': 'testpassword',
        })
        self.assertRedirects(response, reverse('home'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertTrue(get_user_model().objects.filter(email='test@test.com').exists())
        messages_list = list(response.wsgi_request._messages)
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), "Rejestracja przebiegła pomyślnie! Na twój adres e-mail został wysłany link do aktywacji twojego konta.")
    
class SigninTest(TestCase):
        
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            email ="test@test.com",
            password="password",
            first_name = "test",
            is_active = True,
        )
    
    def test_signin_home(self):
        response = self.client.post(reverse('signin'), {
            'email': 'test@test.com',
            'password1': 'password'
        })
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        logout_response = self.client.get(reverse('signout'))

    
    def test_signin_dashboard(self):
        self.user.groups.create(name='Employees')
        response = self.client.post(reverse('signin'), {
            'email': 'test@test.com',
            'password1': 'password'
        })
        self.assertRedirects(response, reverse('dashboard'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

class LogoutTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            email ="test@test.com",
            password="password",
            first_name = "test",
            is_active = True,
        )
         
    def test_signout(self):
        response = self.client.post(reverse('signin'), {
            'email': 'test@test.com',
            'password1': 'password'
        })
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        logout_response = self.client.get(reverse('signout'))
        self.assertRedirects(logout_response, reverse('home'))
        self.assertFalse(logout_response.wsgi_request.user.is_authenticated)
    
    
