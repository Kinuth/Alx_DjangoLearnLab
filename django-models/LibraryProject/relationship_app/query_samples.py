
from relationship_app.models import Author, Book, Library, Librarian


def query_books_by_author(author_name):
    """
    Query all books by a specific author.
    Assumes a model 'Author' and a ForeignKey from 'Book' to 'Author'.
    """
    print(f"--- Query: Books by Author '{author_name}' ---")
    try:
        # 1. Find the specific Author instance
        author_name= Author.objects.get(name=author_name)

        # 2. Query for all Books linked to that Author
        books = Book.objects.filter(author=author_name)

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
        books = Library.objects.get(name=library_name), books.all()

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


def retrieve_librarian(library):
    """
    Retrieve the librarian for a library.
    Assumes a OneToOneField from 'Library' to 'Librarian'.
    """
    print(f"\n--- Query: Librarian for Library '{library}' ---")
    try:
        # 1. Find the specific Library instance, and simultaneously
        #    select the related 'librarian' object to minimize database queries (SELECT_RELATED)
        librarian = Librarian.objects.get(library=library)

        # 2. Access the related Librarian object via the field name
        librarian = Librarian.librarian

        if librarian:
            print(f"The librarian for {library} is: **{librarian.name}**")
            return librarian
        else:
            print(f"No librarian assigned to {library}.")
            return None

    except Library.DoesNotExist:
        print(f"Error: Library named '{library}' not found.")
        return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    # Sample queries
    query_books_by_author("J.K. Rowling")
    list_all_books_in_library("Central Library")
    retrieve_librarian("Central Library")