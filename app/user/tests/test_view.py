"""Test for User views"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from user.models import crete_activation_link

REGISTRATION_URL = reverse('user:registration')


class RegistrationViewTests(TestCase):
    """Tests for registration view"""

    def setUp(self):
        self.email = 'example@example.com'
        self.name = 'TEst name'
        self.password = 'testpassword123'

    def user_registration(self):
        """Registering user with default data"""

        res = self.client.post(REGISTRATION_URL, data={
            'email': self.email,
            'name': self.name,
            'password1': self.password,
            'password2': self.password,
        })
        return res

    def test_get_request_response_ok(self):
        """Test page exist and return 200 status code"""
        res = self.client.get(REGISTRATION_URL)

        self.assertEqual(res.status_code, 200)

    def test_post_request_response_ok(self):
        res = self.client.post(REGISTRATION_URL)

        self.assertEqual(res.status_code, 200)

    def test_redirect_after_successful_post_request(self):
        res = self.user_registration()

        self.assertEqual(res.status_code, 302)

    def test_view_use_correct_template_on_post_request(self):
        """Test registration view use correct html template on post request"""
        res = self.client.post(REGISTRATION_URL)

        self.assertTemplateUsed(res, 'user/registration.html')

    def test_view_use_correct_template_on_get_request(self):
        res = self.client.get(REGISTRATION_URL)

        self.assertTemplateUsed(res, 'user/registration.html')

    def test_only_save_user_then_necessary(self):
        self.client.get(REGISTRATION_URL, data={
            'email': self.email,
            'name': self.name,
            'password1': self.password,
            'password2': self.password,
        })

        user_exist = get_user_model().objects.filter(email=self.email).exists()
        self.assertFalse(user_exist)

    def test_can_save_POST_request(self):
        self.user_registration()

        user_exist = get_user_model().objects.filter(email=self.email).exists()
        self.assertTrue(user_exist)


class ActivationViewTests(TestCase):
    """Test for user activation view"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            name='Test name',
            password='testpassword123'
        )
        self.activation_url = reverse('user:activation_link', args=[
            self.user.activation_link1,
            self.user.activation_link2
        ])

    def test_not_exist_link_raise_error(self):
        """Test raise 404 error on GET request for not existing activation url
        """
        link = reverse('user:activation_link', args=[
            crete_activation_link(),
            crete_activation_link()
        ])
        res = self.client.get(link)

        self.assertEqual(res.status_code, 404)

    def test_exist_link_get_url_response_ok(self):
        """Test exists url GET request returns response code 200"""
        res = self.client.get(self.activation_url)

        self.assertEqual(res.status_code, 200)

    def test_raise_error_only_one_hash_equals(self):
        """Test raise 404 error only one hash int url corresponds user data"""
        link = reverse('user:activation_link', args=[
            self.user.activation_link1,
            crete_activation_link()
        ])

        res = self.client.get(link)

        self.assertEqual(res.status_code, 404)

    def test_get_request_exiting_link_activate_user(self):
        """Test change user is_active parameter to True"""
        self.client.get(self.activation_url)
        self.user.refresh_from_db()

        self.assertTrue(self.user.is_active)

    def test_activate_link_works_only_ones(self):
        """Test raise 404 error on second GET request"""
        res = self.client.get(self.activation_url)

        res = self.client.get(self.activation_url)

        self.assertEqual(res.status_code, 404)
