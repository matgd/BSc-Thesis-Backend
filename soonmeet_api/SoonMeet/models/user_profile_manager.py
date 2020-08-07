from django.contrib.auth.models import BaseUserManager


class UserProfileManager(BaseUserManager):
    """ Manager for user profiles. """

    def create_user(self, username, email, first_name, last_name, password=None):
        # None password won't work because needs hash
        """
        Create user profile.
        :param username: str: username of user
        :param email: str: email of user
        :param first_name: str: name of user
        :param last_name: str: surname of user
        :param password: str: plain user password
        :return: created user
        """
        if not email:
            raise ValueError('User must have an email address.')
        if not first_name:
            raise ValueError('User must have a first name.')
        if not last_name:
            raise ValueError('User must have a surname.')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, first_name=first_name, last_name=last_name)

        user.set_password(password)  # Hashed
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, first_name, last_name, password):
        """ Create and save a new superuser with given details. """
        user = self.create_user(username, email, first_name, last_name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user
