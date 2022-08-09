from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager,
                                        PermissionsMixin)
import hashlib
import random


class UserManager(BaseUserManager):
    """Custom Manager for users"""

    def create_user(self, email, password=None, **extra_fields):
        """Create and return new user"""

        if not email:
            raise ValueError('Users must have an email address')

        if password is None:
            raise ValueError('Users must have a password')

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Create and return superuser"""

        user = self.create_user(email, password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def crete_activation_link():
    hashlib.sha1()
    n = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    a = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
         'l', 'k', 'j', 'h', 'g', 'f', 'd', 's', 'a', 'z',
         'x', 'c', 'v', 'b', 'n', 'm']
    s = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')',
         '_', '+', '}', '{', '|']
    text = ''.join(random.choices(
        n, k=5
    )).join(random.choices(
        a, k=5
    )).join(random.choices(
        s, k=5
    ))
    res = hashlib.sha1(text.encode('utf-8'))
    return res.hexdigest()


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User class"""
    email = models.EmailField(
        max_length=255,
        verbose_name='email address',
        unique=True)
    name = models.CharField(max_length=255, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    activation_link1 = models.CharField(
        max_length=50,
        default=crete_activation_link,
        null=True,
        blank=True)
    activation_link2 = models.CharField(
        max_length=50,
        default=crete_activation_link,
        null=True,
        blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
