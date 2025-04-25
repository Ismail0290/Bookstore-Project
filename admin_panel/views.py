# admin_panel/views.py
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.utils.text import slugify
from books.models import Book, Category
from cart.models import Order, OrderItem

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

class AdminDashboardView(AdminRequiredMixin, View):
    def get(self, request):
        books_count = Book.objects.count()
        categories_count = Category.objects.count()
        orders_count = Order.objects.count()
        recent_orders = Order.objects.order_by('-created_at')[:5]
        
        context = {
            'books_count': books_count,
            'categories_count': categories_count,
            'orders_count': orders_count,
            'recent_orders': recent_orders,
        }
        return render(request, 'admin_panel/dashboard.html', context)

# Book Management Views
class BookListAdminView(AdminRequiredMixin, View):
    def get(self, request):
        books = Book.objects.all().order_by('-created_at')
        context = {
            'books': books,
        }
        return render(request, 'admin_panel/book_list.html', context)

class BookCreateView(AdminRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.all()
        context = {
            'categories': categories,
        }
        return render(request, 'admin_panel/book_form.html', context)
    
    def post(self, request):
        title = request.POST.get('title')
        author = request.POST.get('author')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        category_id = request.POST.get('category')
        isbn = request.POST.get('isbn')
        publication_date = request.POST.get('publication_date')
        cover_image = request.FILES.get('cover_image')
        
        # Validation
        if not (title and author and description and price and stock and category_id and isbn and publication_date):
            messages.error(request, 'All fields are required')
            return redirect('admin_panel:book_create')
        
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            messages.error(request, 'Invalid category')
            return redirect('admin_panel:book_create')
        
        # Create book
        book = Book.objects.create(
            title=title,
            author=author,
            description=description,
            price=price,
            stock=stock,
            category=category,
            isbn=isbn,
            publication_date=publication_date,
            cover_image=cover_image,
        )
        
        messages.success(request, f'Book "{book.title}" created successfully')
        return redirect('admin_panel:book_list')

class BookUpdateView(AdminRequiredMixin, View):
    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        categories = Category.objects.all()
        
        context = {
            'book': book,
            'categories': categories,
        }
        return render(request, 'admin_panel/book_form.html', context)
    
    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        
        title = request.POST.get('title')
        author = request.POST.get('author')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        category_id = request.POST.get('category')
        isbn = request.POST.get('isbn')
        publication_date = request.POST.get('publication_date')
        cover_image = request.FILES.get('cover_image')
        
        # Validation
        if not (title and author and description and price and stock and category_id and isbn and publication_date):
            messages.error(request, 'All fields are required')
            return redirect('admin_panel:book_update', book_id=book_id)
        
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            messages.error(request, 'Invalid category')
            return redirect('admin_panel:book_update', book_id=book_id)
        
        # Update book
        book.title = title
        book.author = author
        book.description = description
        book.price = price
        book.stock = stock
        book.category = category
        book.isbn = isbn
        book.publication_date = publication_date
        
        if cover_image:
            book.cover_image = cover_image
        
        book.save()
        
        messages.success(request, f'Book "{book.title}" updated successfully')
        return redirect('admin_panel:book_list')

class BookDeleteView(AdminRequiredMixin, View):
    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        
        context = {
            'book': book,
        }
        return render(request, 'admin_panel/book_delete.html', context)
    
    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        book_title = book.title
        book.delete()
        
        messages.success(request, f'Book "{book_title}" deleted successfully')
        return redirect('admin_panel:book_list')

# Category Management Views
class CategoryListAdminView(AdminRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.all()
        context = {
            'categories': categories,
        }
        return render(request, 'admin_panel/category_list.html', context)

class CategoryCreateView(AdminRequiredMixin, View):
    def get(self, request):
        return render(request, 'admin_panel/category_form.html')
    
    def post(self, request):
        name = request.POST.get('name')
        
        if not name:
            messages.error(request, 'Name is required')
            return redirect('admin_panel:category_create')
        
        # Create slug
        slug = slugify(name)
        
        # Check if slug exists
        if Category.objects.filter(slug=slug).exists():
            messages.error(request, f'Category with slug "{slug}" already exists')
            return redirect('admin_panel:category_create')
        
        # Create category
        category = Category.objects.create(
            name=name,
            slug=slug,
        )
        
        messages.success(request, f'Category "{category.name}" created successfully')
        return redirect('admin_panel:category_list')

class CategoryUpdateView(AdminRequiredMixin, View):
    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        
        context = {
            'category': category,
        }
        return render(request, 'admin_panel/category_form.html', context)
    
    def post(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        
        name = request.POST.get('name')
        
        if not name:
            messages.error(request, 'Name is required')
            return redirect('admin_panel:category_update', category_id=category_id)
        
        # Create slug
        slug = slugify(name)
        
        # Check if slug exists (excluding current category)
        if Category.objects.filter(slug=slug).exclude(id=category_id).exists():
            messages.error(request, f'Category with slug "{slug}" already exists')
            return redirect('admin_panel:category_update', category_id=category_id)
        
        # Update category
        category.name = name
        category.slug = slug
        category.save()
        
        messages.success(request, f'Category "{category.name}" updated successfully')
        return redirect('admin_panel:category_list')

class CategoryDeleteView(AdminRequiredMixin, View):
    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        
        context = {
            'category': category,
        }
        return render(request, 'admin_panel/category_delete.html', context)
    
    def post(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        category_name = category.name
        
        # Check if category has books
        if category.books.exists():
            messages.error(request, f'Cannot delete category "{category_name}" because it has books')
            return redirect('admin_panel:category_list')
        
        category.delete()
        
        messages.success(request, f'Category "{category_name}" deleted successfully')
        return redirect('admin_panel:category_list')

# Order Management Views
class OrderListAdminView(AdminRequiredMixin, View):
    def get(self, request):
        orders = Order.objects.all().order_by('-created_at')
        context = {
            'orders': orders,
        }
        return render(request, 'admin_panel/order_list.html', context)

class OrderDetailAdminView(AdminRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        
        context = {
            'order': order,
        }
        return render(request, 'admin_panel/order_detail.html', context)

class OrderUpdateStatusView(AdminRequiredMixin, View):
    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        
        status = request.POST.get('status')
        
        if status not in [choice[0] for choice in Order.STATUS_CHOICES]:
            messages.error(request, 'Invalid status')
            return redirect('admin_panel:order_detail', order_id=order_id)
        
        order.status = status
        order.save()
        
        messages.success(request, f'Order #{order.id} status updated to {status}')
        return redirect('admin_panel:order_detail', order_id=order_id)