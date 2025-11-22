from django.db import models

class book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField()

    def __str__(self):
        return self.title


# Alias to provide a `Book` name expected elsewhere in the project
Book = book
