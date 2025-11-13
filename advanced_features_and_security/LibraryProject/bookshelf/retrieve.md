Retrieve Operation
This document details the command used to retrieve an existing Book instance from the database.PrerequisiteFirst, you must import the model:
from bookshelf.models import Book

Command
Assuming the book with title "1984" was already created:
retrieved_book = Book.objects.get(title="1984")

Expected Output:
# Book: 1984 by George Orwell
Or, if you don't have a __str__ method:
# Expected Output:
# <Book: Book object (1)>
If the book is not found, a Book.DoesNotExist exception will be raised.

