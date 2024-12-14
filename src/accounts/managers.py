from django.contrib.auth.models import BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_active, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Email must be set for the user')
        email = self.normalize_email(email)
        now = timezone.now()
        user = self.model(
            email=email,
            is_active=is_active,
            is_staff=is_staff,
            is_superuser=is_superuser,
            last_login=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, first_name='', last_name='', **extra_fields):
        return self._create_user(email, password, is_active=True, is_staff=False, is_superuser=False,
                                 first_name=first_name, last_name=last_name, **extra_fields)

    def create_superuser(self, email, password, first_name='', last_name='', **extra_fields):
        return self._create_user(email, password, is_active=True, is_staff=True, is_superuser=True,
                                 first_name=first_name, last_name=last_name, **extra_fields)
