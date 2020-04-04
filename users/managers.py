# Citation: https://testdriven.io/blog/django-custom-user-model/
from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, access_id, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not access_id:
            raise ValueError('The Access ID must be set')
        user = self.model(access_id=access_id, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, access_id, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        extra_fields.setdefault('legal_name', 'Admin')
        extra_fields.setdefault('age', '0')
        extra_fields.setdefault('legal_gender', 'M')
        extra_fields.setdefault('primary_affiliation', '1')

        return self.create_user(access_id, password, **extra_fields)