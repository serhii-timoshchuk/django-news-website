"""Test for User views"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from user.models import crete_activation_link


REGISTRATION_URL = reverse('user:registration')
LOGOUT_URL = reverse('user:logout')
LOGIN_URL = reverse('user:login')


def create_user(**kwargs):
    """Create and return user"""
    default = {
        'email': 'test@example.com',
        'name': 'test name',
        'password': 'testpassword123',
    }
    default.update(kwargs)
    user = get_user_model().objects.create_user(**default)
    return user


class RegistrationViewTests(TestCase):
    """Tests for registration view"""

    def setUp(self):
        self.email = 'example@example.com'
        self.name = 'TEst name'
        self.password = 'testpassword123'

    def __user_registration(self, **kwargs):
        """Registering user with default data. Returns http response"""

        default = {
            'email': self.email,
            'name': self.name,
            'password1': self.password,
            'password2': self.password,
        }
        default.update(kwargs)

        res = self.client.post(REGISTRATION_URL, data=default)
        return res

    def test_get_request_response_ok(self):
        """Test page exist and return 200 status code"""
        res = self.client.get(REGISTRATION_URL)

        self.assertEqual(res.status_code, 200)

    def test_post_request_response_ok(self):
        res = self.client.post(REGISTRATION_URL)

        self.assertEqual(res.status_code, 200)

    def test_redirect_after_successful_post_request(self):
        res = self.__user_registration()

        self.assertEqual(res.status_code, 302)

    def test_view_use_correct_template_on_post_request(self):
        """Test registration view use correct html template on post request"""
        res = self.client.post(REGISTRATION_URL)

        self.assertTemplateUsed(res, 'user/registration.html')

    def test_view_use_correct_template_on_get_request(self):
        """Test correct template on registration URL GET request"""
        res = self.client.get(REGISTRATION_URL)

        self.assertTemplateUsed(res, 'user/registration.html')

    def test_only_save_user_then_necessary(self):
        """Test dont saves user on GET request"""
        self.client.get(REGISTRATION_URL, data={
            'email': self.email,
            'name': self.name,
            'password1': self.password,
            'password2': self.password,
        })

        user_exist = get_user_model().objects.filter(email=self.email).exists()
        self.assertFalse(user_exist)

    def test_can_save_POST_request(self):
        """Test can save POST request"""
        self.__user_registration()

        user = get_user_model().objects.filter(email=self.email)
        self.assertTrue(user.exists())
        self.assertEqual(user.count(), 1)

    def test_cant_save_user_with_is_active_true(self):
        """Test can`t create user with parameter is_active equals True"""
        self.__user_registration(**{'is_active': True})

        user_exists = get_user_model().objects.filter(
            email=self.email
        ).exists()
        self.assertTrue(user_exists)
        user = get_user_model().objects.get(email=self.email)
        self.assertFalse(user.is_active)

    def test_cant_save_user_with_is_staff_true(self):
        """Test can`t create user with parameter is_staff equals True"""
        self.__user_registration(**{'is_staff': True})

        user_exists = get_user_model().objects.filter(
            email=self.email
        ).exists()
        self.assertTrue(user_exists)
        user = get_user_model().objects.get(email=self.email)
        self.assertFalse(user.is_staff)


class ActivationViewTests(TestCase):
    """Test for user activation view"""

    def setUp(self):
        self.user = create_user()
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


class LoginViewTest(TestCase):
    """Test for log in view"""

    def setUp(self):
        self.good_credentials = {
                'username': 'test@example.com',
                'password': 'testpassword123'
            }
        self.bad_credentials = {
                'username': 'test@example.com',
                'password': 'wrongpass123'
            }
        self.user = create_user(**{
            'email': self.good_credentials['username'],
            'password': self.good_credentials['password'],
            'is_active': True
        }
        )

    def test_login_page_exists(self):
        """Test log in page response 200"""
        res1 = self.client.get(LOGIN_URL)
        res2 = self.client.post(LOGIN_URL)

        self.assertEqual(res1.status_code, 200)
        self.assertEqual(res2.status_code, 200)

    def test_login_page_use_correct_template(self):
        """Test log in view use correct template"""
        res1 = self.client.get(LOGIN_URL)
        res2 = self.client.post(LOGIN_URL)

        self.assertTemplateUsed(res1, 'user/login.html')
        self.assertTemplateUsed(res2, 'user/login.html')

    def test_login_is_successful(self):
        """Test active user can log in"""

        res = self.client.post(
            LOGIN_URL,
            self.good_credentials,
            follow=True)
        self.assertTrue(res.context['user'].is_authenticated)

    def test_raise_error_not_activated_user(self):
        """Test raise error when not activated user try to login"""
        self.user.is_active = False
        self.user.save()
        self.user.refresh_from_db()

        res = self.client.post(
            LOGIN_URL,
            self.good_credentials,
            follow=True)
        self.assertFalse(res.context['user'].is_authenticated)

    def test_redirect_after_login(self):
        """Test redirect after successful POST request"""

        res = self.client.post(
            LOGIN_URL,
            self.good_credentials)
        self.assertEqual(res.status_code, 302)

    def test_login_only_on_post_request(self):
        """Test only POST request make user authorization"""

        res = self.client.get(
            LOGIN_URL,
            self.good_credentials,
            follow=True)
        self.assertFalse(res.context['user'].is_authenticated)

    def test_authenticated_user_cant_login_twice(self):
        """Test authenticated users get a redirect on trying to get a login URL"""
        self.client.post(
            LOGIN_URL,
            self.good_credentials)

        res1 = self.client.get(LOGIN_URL)
        res2 = self.client.post(LOGIN_URL)
        res3 = self.client.post(
            LOGIN_URL,
            self.good_credentials)

        for x in [res1, res2, res3]:
            self.assertEqual(x.status_code, 302)



# add test dont show to authenticated users

# class LogoutViewTest(TestCase):
#     """Tests for logout view"""
#
#     def setUp(self):
#         self.email = 'example@example.com'
#         self.name = 'TEst name'
#         self.password = 'testpassword123'
#
#     def test_raise_redirect_for_unauthenticated_users(self):
#         """Test redirect to login page for unauthenticated users"""
#         res = self.client.get(LOGOUT_URL)
#
#         self.assertEqual(res.status_code, 302)

    # def test_logout_successful(self):
    #     """Test logout successful"""
    #     self.client.post(REGISTRATION_URL, data={
    #         'email': self.email,
    #         'name': self.name,
    #         'password1': self.password,
    #         'password2': self.password,
    #     })
    #
    #     res = self.client.post(LOGOUT_URL)
