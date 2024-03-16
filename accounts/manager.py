from django.contrib.auth.base_user import BaseUserManager
import random
import string

class UserManager(BaseUserManager):
    def create_user(self, phone_number, password = None, **extra_fields):
        if not phone_number:
            raise ValueError("Phone number is required")
        extra_fields.setdefault('email', None)
        extra_fields['email']=self.normalize_email(extra_fields['email'])
        user = self.model(phone_number = phone_number, **extra_fields)
        user.set_password(password)
        user.save(using = self.db)

        return user
    def create_superuser(self, phone_number, password = None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        email = f"{phone_number}@example.com"

        # Append a random string to ensure uniqueness
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        email_with_random = f"{email}-{random_string}"
        extra_fields.setdefault('email', email_with_random)

        return self.create_user(phone_number, password=password, **extra_fields)