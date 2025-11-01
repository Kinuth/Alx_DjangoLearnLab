Update Operation
This document details the commands used to update an existing Book instance.Prerequisite
First, you must import the model:
from bookshelf.models import Book

Commands
Retrieve the book you want to update (e.g., the one with title "1984").
book_to_update = Book.objects.get(title="1984")

Modify the attribute (e.g., the title).
book_to_update.title = "Nineteen Eighty-Four"

Save the changes back to the database.
book_to_update.save()

Expected Output
After saving, the object in the database is updated. If you retrieve and print the object again using its ID:
updated_book = Book.objects.get(id=book_to_update.id)
print(updated_book)

The shell will output the new string representation:
# Expected Output:
# Book: Nineteen Eighty-Four by George Orwell
Or, if you don't have a __str__ method:
# Expected Output:
# <Book: Book object (1)>
(Note: The object itself is updated, showing the new title.)