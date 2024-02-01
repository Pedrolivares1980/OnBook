from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Book
from .forms import BookForm
from django.utils import timezone
import datetime


class BookModelTest(TestCase):
    """Tests for the Book model."""

    def setUp(self):
        self.book = Book.objects.create(
            name="Test Book",
            author="Test Author",
            publisher="Test Publisher",
            publish_date=timezone.now().date(),
            language="English",
            category="novel",
            description="Test Description",
            is_available=True,
        )

    def test_model_str(self):
        self.assertEqual(str(self.book), "Test Book")


class BookListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_books = 13
        for book_num in range(number_of_books):
            Book.objects.create(
                name=f"Book {book_num}",
                author="Author",
                publisher="Publisher",
                publish_date=timezone.now().date(),
                language="English",
                category="novel",
                description="Description",
                is_available=True,
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/books/list/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("book_list"))
        self.assertEqual(response.status_code, 200)

    def test_pagination_is_five(self):
        response = self.client.get(reverse("book_list"))
        self.assertTrue("is_paginated" in response.context)
        self.assertEqual(len(response.context["books"]), 5)

    def test_lists_all_books(self):
        response = self.client.get(reverse("book_list") + "?page=3")
        self.assertEqual(len(response.context["books"]), 3)


class BookDetailViewTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            name="Test Book Detail",
            author="Test Author",
            publisher="Test Publisher",
            publish_date=timezone.now().date(),
            language="English",
            category="novel",
            description="Test Description Detail",
            is_available=True,
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f"/books/{self.book.id}/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("book_detail", args=[self.book.id]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("book_detail", args=[self.book.id]))
        self.assertTemplateUsed(response, "books/book_detail.html")

    def test_view_displays_correct_book_details(self):
        response = self.client.get(reverse("book_detail", args=[self.book.id]))
        self.assertEqual(response.context["book"].id, self.book.id)
        self.assertEqual(response.context["book"].name, "Test Book Detail")


class BookFormTest(TestCase):
    def test_form_validity(self):
        form_data = {
            "name": "New Book",
            "author": "Author",
            "publisher": "Publisher",
            "publish_date": timezone.now().date(),
            "language": "English",
            "category": "novel",
            "description": "Description",
            "is_available": True,
        }
        form = BookForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalidity_with_future_publish_date(self):
        future_date = timezone.now().date() + datetime.timedelta(days=30)
        form_data = {
            "name": "Future Book",
            "author": "Author",
            "publisher": "Publisher",
            "publish_date": future_date,
            "language": "English",
            "category": "novel",
            "description": "Future Description",
            "is_available": True,
        }
        form = BookForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("publish_date", form.errors)


class BookCreateViewTest(TestCase):
    """Tests for the book creation view."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="12345", is_staff=True
        )
        self.client.login(username="testuser", password="12345")

    def test_create_view_access(self):
        response = self.client.get(reverse("book_add"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "books/book_form.html")

    def test_create_book(self):
        book_data = {
            "name": "New Book",
            "author": "Author",
            "publisher": "Publisher",
            "publish_date": timezone.now().date(),
            "language": "English",
            "category": "novel",
            "description": "Description",
            "is_available": True,
        }
        response = self.client.post(reverse("book_add"), book_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Book.objects.filter(name="New Book").exists())


class BookUpdateViewTest(TestCase):
    """Tests for the book update view."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="12345", is_staff=True
        )
        self.client.login(username="testuser", password="12345")
        self.book = Book.objects.create(
            name="Test Book",
            author="Test Author",
            publisher="Test Publisher",
            publish_date="2022-01-01",
            language="Test Language",
            category="Test Category",
            description="Test Description",
            is_available=True,
        )

    def test_update_view_access(self):
        response = self.client.get(reverse("book_update", args=[self.book.id]))
        self.assertEqual(response.status_code, 200)

    def test_update_book(self):
        updated_data = {
            "name": "Updated Book",
            "author": "Updated Author",
            "publisher": "Updated Publisher",
            "publish_date": timezone.now().date(),
            "language": "Updated Language",
            "category": "novel",
            "description": "Updated Description",
            "is_available": True,
        }
        response = self.client.post(
            reverse("book_update", args=[self.book.id]), updated_data
        )
        self.assertEqual(response.status_code, 302)
        updated_book = Book.objects.get(id=self.book.id)
        self.assertEqual(updated_book.name, "Updated Book")


class BookDeleteViewTest(TestCase):
    """Tests for the book delete view."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="12345", is_staff=True
        )
        self.client.login(username="testuser", password="12345")
        self.book = Book.objects.create(
            name="Test Book",
            author="Test Author",
            publisher="Test Publisher",
            publish_date=timezone.now().date(),
            language="English",
            category="novel",
            description="Test Description",
            is_available=True,
        )

    def test_delete_view_access(self):
        response = self.client.get(reverse("book_delete", args=[self.book.id]))
        self.assertEqual(response.status_code, 200)

    def test_delete_book(self):
        response = self.client.post(reverse("book_delete", args=[self.book.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())


class BookFormTest(TestCase):
    """Tests for the BookForm."""

    def test_form_validity(self):
        """Test the validity of the form with correct data."""
        form_data = {
            "name": "New Book",
            "author": "Author",
            "publisher": "Publisher",
            "publish_date": timezone.now().date(),
            "language": "English",
            "category": "novel",
            "description": "Description",
            "is_available": True,
        }
        form = BookForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalidity_missing_name(self):
        """Test form invalidity with missing 'name'."""
        form_data = {
            "author": "Test Author",
            "publisher": "Test Publisher",
            "publish_date": "2021-01-01",
            "language": "English",
            "category": "novel",
            "description": "Test Description",
            "is_available": True,
        }
        form = BookForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_invalidity_invalid_publish_date(self):
        """Test form invalidity with invalid 'publish_date'."""
        form_data = {
            "name": "Test Book",
            "author": "Test Author",
            "publisher": "Test Publisher",
            "publish_date": "invalid_date_format",
            "language": "English",
            "category": "novel",
            "description": "Test Description",
            "is_available": True,
        }
        form = BookForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_invalidity_missing_category(self):
        # Test with missing 'category'
        form_data = {
            "name": "Test Book",
            "author": "Test Author",
            "publisher": "Test Publisher",
            "publish_date": "2021-01-01",
            "language": "English",
            "description": "Test Description",
            "is_available": True,
        }
        form = BookForm(data=form_data)
        self.assertTrue(form.is_valid())
