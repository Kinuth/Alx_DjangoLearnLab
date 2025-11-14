Delete Operation
This document details the commands used to delete an existing Book instance.Prerequisite
First, you must import the model:
from bookshelf.models import Book

Commands
Retrieve the book you want to delete (e.g., the one with the updated title "Nineteen Eighty-Four").
book_to_delete = Book.objects.get(title="Nineteen Eighty-Four")

Call the delete() method on the object.
book.delete()

Expected Output
The delete() command will return a tuple indicating the number of objects deleted and a dictionary with the count per object type.
# Expected Output:
# (1, {'bookshelf.Book': 1})
If you then try to retrieve the same book, the database will raise an error because it no longer exists.
try:
    Book.objects.get(title="Nineteen Eighty-Four")
except Book.DoesNotExist:
    print("Book successfully deleted and cannot be found.")

The expected output from this try...except block is:
# Expected Output:
# Book successfully deleted and cannot be found.
