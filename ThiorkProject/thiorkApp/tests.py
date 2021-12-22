from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from thiorkApp.models import Vectis, Servitium

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


class ServitiumTestCase(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'b[Z9rpH$'}
        Vectis.objects.create_user(**self.credentials)

    def test_create_servitium(self):
        user = Vectis.objects.first()
        Servitium.objects.create(owner=user, title='Oil Refill', description="I'll show you how to refill the oil in your car.", location='41.036944,28.9775', credit=1)

        self.assertTrue(Servitium.objects.exists(), True)
        self.assertEqual(Servitium.objects.latest('publish_date').status, 'Available')


class VectisTestCase(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'b[Z9rpH$'}
        Vectis.objects.create_user(**self.credentials)

    def test_vectis_has_five_credit(self):
        user = Vectis.objects.first()

        self.assertEqual(user.credit, 5)
