from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
# --- TASK 1: CUSTOM USER MANAGER ---

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        from django.db import models
        from django.contrib.auth.models import AbstractUser, BaseUserManager
        from django.utils.translation import gettext_lazy as _


        # --- TASK 1: CUSTOM USER MANAGER ---


        class CustomUserManager(BaseUserManager):
            """
            Custom user model manager where email is the unique identifier
            for authentication instead of usernames.
            """

            def create_user(self, email, password=None, **extra_fields):
                """
                Create and save a User with the given email and password.
                """
                if not email:
                    raise ValueError(_('The Email must be set'))
                email = self.normalize_email(email)
                user = self.model(email=email, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user

            def create_superuser(self, email, password, **extra_fields):
                """
                Create and save a SuperUser with the given email and password.
                """
                extra_fields.setdefault('is_staff', True)
                extra_fields.setdefault('is_superuser', True)
                extra_fields.setdefault('is_active', True)

                if extra_fields.get('is_staff') is not True:
                    raise ValueError(_('Superuser must have is_staff=True.'))
                if extra_fields.get('is_superuser') is not True:
                    raise ValueError(_('Superuser must have is_superuser=True.'))
                return self.create_user(email, password, **extra_fields)


        # --- TASK 1: CUSTOM USER MODEL ---


        class CustomUser(AbstractUser):
            """
            Custom User Model extending AbstractUser.
            We remove the username field and use email as the unique identifier.
            """
            # Remove username field from default AbstractUser
            username = None

            # Make email the unique identifier and required
            email = models.EmailField(_('email address'), unique=True)

            # Add custom fields
            date_of_birth = models.DateField(null=True, blank=True)
            profile_photo = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

            # Set the unique identifier field for login
            USERNAME_FIELD = 'email'

            # Fields required when creating a user via createsuperuser
            REQUIRED_FIELDS = []

            # Tell Django to use our CustomUserManager
            objects = CustomUserManager()

            def __str__(self):
                return self.email


        # --- TASK 2: MODEL WITH CUSTOM PERMISSIONS ---


        class Book(models.Model):
            title = models.CharField(max_length=200)
            author = models.CharField(max_length=200)
            publication_year = models.IntegerField(null=True, blank=True)

            class Meta:
                # Define custom permissions for the Book model
                permissions = [
                    ("can_view", "Can view book"),
                    ("can_create", "Can create book"),
                    ("can_edit", "Can edit book"),
                    ("can_delete", "Can delete book"),
                ]

            def __str__(self):
                return self.title
