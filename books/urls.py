# books/urls.py
from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.BookListView.as_view(), name='book_list'),
    path('category/<slug:category_slug>/', views.BookListView.as_view(), name='book_list_by_category'),
    path('book/<int:book_id>/', views.BookDetailView.as_view(), name='book_detail'),
]