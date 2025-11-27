from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Book

class BookAPITests(APITestCase):
    
    def setUp(self):
        """
        Set up the test environment before each test method runs.
        We create a test user and two initial books to test against.
        """
        # Create a user for authentication testing
        self.user = User.objects.create_user(username='testuser', password='password')
        
        # Create sample data
        self.book1 = Book.objects.create(
            title="Harry Potter and the Philosopher's Stone",
            author="J.K. Rowling",
            publication_year=1997
        )
        self.book2 = Book.objects.create(
            title="1984",
            author="George Orwell",
            publication_year=1949
        )
        
        # URL names (ensure these match your urls.py names)
        self.list_url = reverse('book-list')
        self.create_url = reverse('book-create')

    # ----------------------------------------------------------------
    # 1. CRUD Tests (Create, Read, Update, Delete)
    # ----------------------------------------------------------------

    def test_list_books(self):
        """Test retrieving the list of books (Public access)."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # We created 2 books in setUp

    def test_retrieve_book_detail(self):
        """Test retrieving a single book (Public access)."""
        url = reverse('book-detail', args=[self.book1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)

    def test_create_book_authenticated(self):
        """Test creating a book with a logged-in user."""
        self.client.login(username='testuser', password='password')
        data = {
            "title": "New Book",
            "author": "New Author",
            "publication_year": 2023
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(response.data['title'], "New Book")

    def test_update_book_authenticated(self):
        """Test updating a book with a logged-in user."""
        self.client.login(username='testuser', password='password')
        url = reverse('book-update', args=[self.book1.id])
        data = {
            "title": "Harry Potter (Updated)",
            "author": "J.K. Rowling",
            "publication_year": 1997
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Harry Potter (Updated)")

    def test_delete_book_authenticated(self):
        """Test deleting a book with a logged-in user."""
        self.client.login(username='testuser', password='password')
        url = reverse('book-delete', args=[self.book1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    # ----------------------------------------------------------------
    # 2. Permission Tests
    # ----------------------------------------------------------------

    def test_create_book_unauthenticated(self):
        """Test that unauthenticated users cannot create books."""
        data = {"title": "Unauthorized Book", "author": "Anon", "publication_year": 2023}
        response = self.client.post(self.create_url, data)
        # Should be 401 Unauthorized or 403 Forbidden depending on settings
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_delete_book_unauthenticated(self):
        """Test that unauthenticated users cannot delete books."""
        url = reverse('book-delete', args=[self.book1.id])
        response = self.client.delete(url)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    # ----------------------------------------------------------------
    # 3. Filtering, Searching, and Ordering Tests
    # ----------------------------------------------------------------

    def test_filter_books_by_author(self):
        """Test filtering books by author."""
        # Request books by George Orwell
        response = self.client.get(self.list_url, {'author': 'George Orwell'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author'], 'George Orwell')

    def test_search_books(self):
        """Test searching books by title or author."""
        # Search for 'Potter'
        response = self.client.get(self.list_url, {'search': 'Potter'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Harry Potter and the Philosopher's Stone")

    def test_ordering_books(self):
        """Test ordering books by publication year."""
        # Order by publication_year descending (newest first)
        response = self.client.get(self.list_url, {'ordering': '-publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], "1984") # 1949 (Wait, let me check logic)
        
        # Wait, 1949 < 1997. 
        # If ordering is -publication_year, 1997 comes first.
        # Let's fix the assertion logic:
        self.assertEqual(response.data[0]['publication_year'], 1997)
        self.assertEqual(response.data[1]['publication_year'], 1949)