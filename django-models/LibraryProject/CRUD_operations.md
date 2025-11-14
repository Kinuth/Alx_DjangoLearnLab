1.Create Operation
This document details the command used to create a new Book instance in the Django shell.PrerequisiteFirst, you must import the model:
from bookshelf.models import Book

Command
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)

Expected Output
After running the create command, a new Book object is created in the database and returned. If you print the book variable:
print(book)
The shell will output the string representation of the object 
book= 1984

2.Retrieve Operation
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

3.Update Operation
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

4.Delete Operation
This document details the commands used to delete an existing Book instance.Prerequisite
First, you must import the model:
from bookshelf.models import Book

Commands
Retrieve the book you want to delete (e.g., the one with the updated title "Nineteen Eighty-Four").
book_to_delete = Book.objects.get(title="Nineteen Eighty-Four")

Call the delete() method on the object.
book_to_delete.delete()

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
