from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .user_profile_manager import UserProfileManager


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """ Database model for users in the system. """
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    last_modified = models.DateTimeField(auto_now=True)

    objects = UserProfileManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']  # username is default ^

    def get_full_name(self):
        """
        Retrieve full name of user (name and surname).
        :return: full name of user
        """
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        """
        Retrieve short name of user (first name).
        :return: short name of user
        """
        return self.first_name
