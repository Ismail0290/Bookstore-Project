from django.test import TestCase
from django.urls import reverse
from .models import Book, Category

class BookModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Fiction", slug="fiction")
        self.book = Book.objects.create(title="Test Book", category=self.category)

    def test_book_creation(self):
        self.assertEqual(self.book.title, "Test Book")
        self.assertEqual(self.book.category.name, "Fiction")

    def test_book_list_view(self):
        response = self.client.get(reverse("books:book_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Book")
