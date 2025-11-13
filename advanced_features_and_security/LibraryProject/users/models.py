from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """
    
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email, password, and custom fields.
        """
        if not email:
            raise ValueError('The Email must be set')
        
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
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        # We don't require custom fields for superusers, so we just call create_user
        return self.create_user(email, password, **extra_fields)


# --- Step 1: Set Up the Custom User Model ---
class CustomUser(AbstractUser):
    """
    Extends AbstractUser to add custom fields.
    """
    # We remove the username field and make email the primary identifier
    username = None
    email = models.EmailField('email address', unique=True)

    # Add our new custom fields
    date_of_birth = models.DateField(null=True, blank=True)
    
    # NOTE: ImageField requires 'Pillow' library (pip install Pillow)
    # 'upload_to' specifies the subdirectory within MEDIA_ROOT
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    # Set the email field as the username field
    USERNAME_FIELD = 'email'
    
    # Fields required when creating a user via createsuperuser
    # email and password are required by default.
    REQUIRED_FIELDS = ['first_name', 'last_name'] 

    # Link the model to its custom manager
    objects = CustomUserManager()

    def __str__(self):
        return self.email