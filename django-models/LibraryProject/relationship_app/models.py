from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=200)  
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    class Meta:
        # Define the custom permissions here
        permissions = [
            ("can_add_book", "Can add a new book entry"),
            ("can_change_book", "Can edit existing book entries"),
            ("can_delete_book", "Can delete book entries"),
        ]
        ordering = ['title']

    def __str__(self):
        return self.title   
class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book, related_name='libraries')
    def __str__(self):
        return self.name
class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name='librarian')
    def __str__(self):
        return self.name
    


class UserProfile(models.Model):
    """
    Extends the default User model to include a role.
    """
    # Define role choices
    class Role(models.TextChoices):
        ADMIN = 'Admin', 'Admin'
        LIBRARIAN = 'Librarian', 'Librarian'
        MEMBER = 'Member', 'Member'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=Role.choices , default='Member')

    def __str__(self):
        return f"{self.user.username} - {self.role}"

# Automatic Creation using Signals
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # This assumes you have already run the initial migration and created the UserProfile table
    # It attempts to get the profile and saves it.
    try:
        instance.profile.save()
    except UserProfile.DoesNotExist:
        # If the user was created *before* the UserProfile model existed,
        # we create it here instead of relying solely on the 'created' check.
        UserProfile.objects.create(user=instance)