"""
Test for User Forms
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from user.forms import CustomAuthenticationForm, CustomUserCreationForm


class CustomAuthenticationFormTests(TestCase):
    """Tests for custom user authentication form"""

    def setUp(self):
        self.email = 'text@example.com'
        self.password = 'testpassword123'
        self.user = get_user_model().objects.create_user(
            email=self.email,
            password=self.password)

    def test_authentication_form_valid(self):
        """Test authentication form is valid for active users"""
        self.user.is_active = True
        self.user.save()
        form = CustomAuthenticationForm(data={
            'username': self.email,
            'password': self.password
        })
        self.assertTrue(form.is_valid())

    def test_authentication_form_error_not_active_user(self):
        """Test authenticationForm raise error for registered
         but not active users"""
        form = CustomAuthenticationForm(data={
            'username': self.email,
            'password': self.password
        })
        self.assertFalse(form.is_valid())

    def test_authentication_form_error_unexisting_user(self):
        """Test authenticationForm raise error for unexisting users"""
        form = CustomAuthenticationForm(data={
            'username': 'emailwrong@example.com',
            'password': self.password}
        )
        self.assertFalse(form.is_valid())

    def test_authentication_form_value_error(self):
        """Test authenticationForm raise error for unexisting users"""
        form1 = CustomAuthenticationForm(data={'username': self.email})
        form2 = CustomAuthenticationForm(data={'password': self.password})
        form3 = CustomAuthenticationForm(data={
            'username': self.email,
            'password': 'passwordwrong'
        })
        self.assertFalse(form1.is_valid())
        self.assertFalse(form2.is_valid())
        self.assertFalse(form3.is_valid())


class CustomUserCreationFormTests(TestCase):
    """Test for custom creating form"""

    def setUp(self):
        self.USER_DATA = {
            'email': 'example@example.com',
            'name': 'TEst name',
            'password1': 'testpaswrosd123',
            'password2': 'testpaswrosd123'
        }

    def test_user_creation_form_is_valid(self):
        """Test creating user form is valid"""
        form = CustomUserCreationForm(data=self.USER_DATA)
        self.assertTrue(form.is_valid())

    def test_user_creation_form_can_create_user(self):
        """Test creating user form is valid"""
        form = CustomUserCreationForm(data=self.USER_DATA)
        self.assertTrue(form.is_valid())
        form.save()
        user_exists = get_user_model().objects.filter(
            email=self.USER_DATA['email']
        ).exists()
        self.assertTrue(user_exists)

    def test_user_creation_form_error_with_existing_user(self):
        """Test form not valid when user email already exists"""
        get_user_model().objects.create_user(
            email='example@example.com',
            password='testpaswrosd123'
        )
        form = CustomUserCreationForm(data=self.USER_DATA)
        self.assertFalse(form.is_valid())

    def test_user_creation_form_error_passwords_missmatch(self):
        """Test raise error on passwords missmatch"""
        case1 = self.USER_DATA
        case1['password1'] = 'missmatch123'
        form = CustomUserCreationForm(data=case1)
        self.assertFalse(form.is_valid())

    def test_user_creation_form_error_without_required_data(self):
        """Test return error if not all required fields have the data"""
        case1, case2, case3 = self.USER_DATA, self.USER_DATA, self.USER_DATA
        case1['email'] = ''
        case2['password1'] = ''
        case3['password2'] = ''
        form1 = CustomUserCreationForm(data=case1)
        form2 = CustomUserCreationForm(data=case2)
        form3 = CustomUserCreationForm(data=case3)
        self.assertFalse(form1.is_valid())
        self.assertFalse(form2.is_valid())
        self.assertFalse(form3.is_valid())
