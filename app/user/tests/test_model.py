"""Tests for User model"""
from django.db.utils import IntegrityError
from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTests(TestCase):
    """Tests for User model"""

    def test_create_user(self):
        """Test creating user is successful."""
        email = 'test@example.com'
        password = 'goodpassword123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_user_is_active_false(self):
        """Test user creates with is_active equal False"""
        email = 'test@example.com'
        password = 'goodpassword123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.is_active, False)

    def test_create_user_without_email_raises_error(self):
        """Test return error on creating user without email."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', '1123sample')

    def test_create_user_without_password_raises_error(self):
        """Test return error on creating user without email."""
        email = 'test@example.com"'
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=email)
        self.assertFalse(get_user_model().objects.filter(email=email).exists())

    def test_create_user_with_exist_email_raises_error(self):
        """Test return error in creating user with exist email."""
        email = 'test@example.com'
        get_user_model().objects.create_user(
            email=email,
            password='1123sample',
            name='Test name'
        )
        with self.assertRaises(IntegrityError):
            get_user_model().objects.create_user(
                email='test@example.com',
                password='1123sample',
                name="Changeme")

    def test_new_user_email_normalized(self):
        """Test user email is normalized."""
        sample_emails = [
            ['test1@example.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@EXAMPLE.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(
                email=email,
                password='password123w'
            )
            self.assertEqual(user.email, expected)

    def test_creates_activated_link_with_create_user(self):
        """Test creates activated link on user creation"""
        email = 'test@example.com'
        password = 'goodpassword123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertNotEqual(user.activation_link1, None)
        self.assertNotEqual(user.activation_link2, None)

    def test_create_super_user(self):
        """Test creating superuser is successful."""
        email = 'test@example.com'
        password = 'test123password'
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
