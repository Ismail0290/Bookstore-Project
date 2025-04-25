# admin_panel/urls.py
from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.AdminDashboardView.as_view(), name='dashboard'),
    
    # Book management
    path('books/', views.BookListAdminView.as_view(), name='book_list'),
    path('books/create/', views.BookCreateView.as_view(), name='book_create'),
    path('books/update/<int:book_id>/', views.BookUpdateView.as_view(), name='book_update'),
    path('books/delete/<int:book_id>/', views.BookDeleteView.as_view(), name='book_delete'),
    
    # Category management
    path('categories/', views.CategoryListAdminView.as_view(), name='category_list'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('categories/update/<int:category_id>/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('categories/delete/<int:category_id>/', views.CategoryDeleteView.as_view(), name='category_delete'),
    
    # Order management
    path('orders/', views.OrderListAdminView.as_view(), name='order_list'),
    path('orders/<int:order_id>/', views.OrderDetailAdminView.as_view(), name='order_detail'),
    path('orders/<int:order_id>/update-status/', views.OrderUpdateStatusView.as_view(), name='order_update_status'),
]