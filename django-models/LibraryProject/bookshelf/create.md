Create Operation
This document details the command used to create a new Book instance in the Django shell.PrerequisiteFirst, you must import the model:
from bookshelf.models import Book

Command
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)

Expected Output
After running the create command, a new Book object is created in the database and returned. If you print the book variable:
print(book)
The shell will output the string representation of the object 
book= 1984