
from relationship_app.models import Author, Book, Library, Librarian


def query_books_by_author(author_name):
    """
    Query all books by a specific author.
    Assumes a model 'Author' and a ForeignKey from 'Book' to 'Author'.
    """
    print(f"--- Query: Books by Author '{author_name}' ---")
    try:
        # 1. Find the specific Author instance
        author_instance = Author.objects.get(name__iexact=author_name)

        # 2. Query for all Books linked to that Author
        books = Book.objects.filter(author=author_instance)

        print(f"Found {books.count()} books by {author_name}:")
        for book in books:
            print(f"- {book.title}")
        return books

    except Author.DoesNotExist:
        print(f"Error: Author named '{author_name}' not found.")
        return []

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def list_all_books_in_library(library_name):
    """
    List all books in a specific library.
    Assumes a model 'Library' and a ForeignKey from 'Book' to 'Library'.
    """
    print(f"\n--- Query: Books in Library '{library_name}' ---")
    try:
        # 1. Find the specific Library instance
        library_instance = Library.objects.get(name__iexact=library_name)

        # 2. Query for all Books linked to that Library
        # Using the reverse relationship manager (set by default by Django ORM)
        books = library_instance.book_set.all()

        # Alternatively, using a direct filter on the Book model:
        # books = Book.objects.filter(library=library_instance)

        print(f"Found {books.count()} books in {library_name}:")
        for book in books:
            print(f"- {book.title} (Author: {book.author.name})")
        return books

    except Library.DoesNotExist:
        print(f"Error: Library named '{library_name}' not found.")
        return []

    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def retrieve_librarian_for_library(library_name):
    """
    Retrieve the librarian for a library.
    Assumes a OneToOneField from 'Library' to 'Librarian'.
    """
    print(f"\n--- Query: Librarian for Library '{library_name}' ---")
    try:
        # 1. Find the specific Library instance, and simultaneously
        #    select the related 'librarian' object to minimize database queries (SELECT_RELATED)
        library_instance = Library.objects.select_related('librarian').get(name__iexact=library_name)

        # 2. Access the related Librarian object via the field name
        librarian_instance = library_instance.librarian

        if librarian_instance:
            print(f"The librarian for {library_name} is: **{librarian_instance.name}**")
            return librarian_instance
        else:
            print(f"No librarian assigned to {library_name}.")
            return None

    except Library.DoesNotExist:
        print(f"Error: Library named '{library_name}' not found.")
        return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    # Sample queries
    query_books_by_author("J.K. Rowling")
    list_all_books_in_library("Central Library")
    retrieve_librarian_for_library("Central Library")