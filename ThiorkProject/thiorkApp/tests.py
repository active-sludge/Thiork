from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from thiorkApp.models import Vectis

c = Client()


class ViewTestsCase(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'b[Z9rpH$'}
        Vectis.objects.create_user(**self.credentials)

    def test_home_page_accessed_successfully(self):
        response = c.get('/')
        self.assertEqual(response.status_code, 200)

    def test_user_lands_on_home_after_login(self):
        c.login(username='testuser', password='b[Z9rpH$')
        response = self.client.get(reverse('servitiums'))
        self.assertEqual(response.status_code, 200)

    def test_view_url_exists_at_desired_location(self):
        c.login(username='testuser', password='b[Z9rpH$')
        response = self.client.get(reverse('servitiums'))
        self.assertEqual(response.status_code, 200)


class LogInTestCase(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'b[Z9rpH$'}
        Vectis.objects.create_user(**self.credentials)

    def test_login(self):
        # send login data
        response = self.client.post('/login', self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_active)
