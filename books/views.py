# books/views.py
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Book, Category

class BookListView(View):
    def get(self, request, category_slug=None):
        categories = Category.objects.all()
        
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            books = Book.objects.filter(category=category)
        else:
            books = Book.objects.all()
        
        context = {
            'categories': categories,
            'books': books,
        }
        return render(request, 'books/book_list.html', context)

class BookDetailView(View):
    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        context = {
            'book': book,
        }
        return render(request, 'books/book_detail.html', context)