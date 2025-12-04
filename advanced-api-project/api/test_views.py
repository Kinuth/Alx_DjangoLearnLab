from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Book, Author  

class BookAPITests(APITestCase):
    
    def setUp(self):
        """
        Set up the test environment.
        Fix 2: We must create Author instances FIRST, then assign them to Books.
        """
        self.user = User.objects.create_user(username='testuser', password='password')
        
        # Create Author Instances
        self.author1 = Author.objects.create(name="J.K. Rowling")
        self.author2 = Author.objects.create(name="George Orwell")
        
        # Create Book Instances (Assigning the Author objects, not strings)
        self.book1 = Book.objects.create(
            title="Harry Potter and the Philosopher's Stone",
            author=self.author1, # Pass the object instance
            publication_year=1997
        )
        self.book2 = Book.objects.create(
            title="1984",
            author=self.author2, # Pass the object instance
            publication_year=1949
        )
        
        self.list_url = reverse('book-list')
        self.create_url = reverse('book-create')

    def test_list_books(self):
        """Test retrieving the list of books."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_book_detail(self):
        """Test retrieving a single book."""
        url = reverse('book-detail', args=[self.book1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)

    def test_create_book_authenticated(self):
        """Test creating a book."""
        self.client.login(username='testuser', password='password')
        
        # We need a new author for this test
        new_author = Author.objects.create(name="New Test Author")
        
        data = {
            "title": "New Book",
            "author": new_author.id,
            "publication_year": 2023
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(response.data['title'], "New Book")

    def test_update_book_authenticated(self):
        """Test updating a book."""
        self.client.login(username='testuser', password='password')
        url = reverse('book-update', args=[self.book1.id])
        
        data = {
            "title": "Harry Potter (Updated)",
            "author": self.author1.id, # Keep the same author ID
            "publication_year": 1997
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Harry Potter (Updated)")

    def test_delete_book_authenticated(self):
        """Test deleting a book."""
        self.client.login(username='testuser', password='password')
        url = reverse('book-delete', args=[self.book1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_create_book_unauthenticated(self):
        """Test unauthenticated create fail."""
        data = {
            "title": "Unauthorized Book", 
            "author": self.author1.id, 
            "publication_year": 2023
        }
        response = self.client.post(self.create_url, data)
        # Expecting 403 Forbidden or 401 Unauthorized depending on specific DRF settings
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_delete_book_unauthenticated(self):
        """Test unauthenticated delete fail."""
        url = reverse('book-delete', args=[self.book1.id])
        response = self.client.delete(url)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    # ----------------------------------------------------------------
    # Filter Tests
    # ----------------------------------------------------------------

    def test_filter_books_by_author(self):
        """Test filtering books by author."""
        # Note: If your filter backend uses exact ID matching:
        response = self.client.get(self.list_url, {'author': self.author2.id})
        
        # If your filter backend uses name search (depends on views.py setup):
        # response = self.client.get(self.list_url, {'author': 'George Orwell'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that we got at least one book back
        self.assertTrue(len(response.data) > 0)
        # Check that the book returned is indeed 1984
        self.assertEqual(response.data[0]['title'], '1984')

    def test_search_books(self):
        """Test searching books."""
        response = self.client.get(self.list_url, {'search': 'Potter'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Harry Potter and the Philosopher's Stone")

    def test_ordering_books(self):
        """Test ordering books."""
        response = self.client.get(self.list_url, {'ordering': 'publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 1949 (Index 0) comes before 1997 (Index 1)
        self.assertEqual(response.data[0]['publication_year'], 1949)
        self.assertEqual(response.data[1]['publication_year'], 1997)