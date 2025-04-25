# cart/views.py
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from decimal import Decimal
from books.models import Book
from .models import Order, OrderItem

class CartView(View):
    def get(self, request):
        cart = request.session.get('cart', {})
        cart_items = []
        total_price = Decimal('0.00')
        
        for book_id, quantity in cart.items():
            book = get_object_or_404(Book, id=book_id)
            price = book.price * Decimal(quantity)
            total_price += price
            cart_items.append({
                'book': book,
                'quantity': quantity,
                'price': price,
            })
        
        context = {
            'cart_items': cart_items,
            'total_price': total_price,
        }
        return render(request, 'cart/cart.html', context)

class AddToCartView(View):
    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        try:
            quantity = int(request.POST.get('quantity', 1))
        except (ValueError, TypeError):
            quantity = 1
            
        if quantity <= 0:
            messages.error(request, 'Quantity must be positive')
            return redirect('books:book_detail', book_id=book_id)
        
        if quantity > book.stock:
            messages.error(request, 'Not enough books in stock')
            return redirect('books:book_detail', book_id=book_id)
        
        cart = request.session.get('cart', {})
        cart[str(book_id)] = cart.get(str(book_id), 0) + quantity
        
        # Ensure we don't exceed stock
        if cart[str(book_id)] > book.stock:
            cart[str(book_id)] = book.stock
            messages.warning(request, f'Adjusted quantity to available stock ({book.stock})')
        
        request.session['cart'] = cart
        request.session.modified = True
        
        messages.success(request, f'Added {quantity} copies of "{book.title}" to your cart')
        return redirect(request.META.get('HTTP_REFERER', 'cart:cart'))
        
class UpdateCartView(View):
    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity <= 0:
            messages.error(request, 'Quantity must be positive')
            return redirect('cart:cart')
        
        if quantity > book.stock:
            messages.error(request, 'Not enough books in stock')
            return redirect('cart:cart')
        
        # Get cart
        cart = request.session.get('cart', {})
        
        # Update quantity
        cart[str(book_id)] = quantity
        
        # Save cart to session
        request.session['cart'] = cart
        request.session.modified = True
        
        messages.success(request, 'Cart updated successfully')
        return redirect('cart:cart')

class RemoveFromCartView(View):
    def post(self, request, book_id):
        # Get cart
        cart = request.session.get('cart', {})
        
        # Remove item
        if str(book_id) in cart:
            del cart[str(book_id)]
            
            # Save cart to session
            request.session['cart'] = cart
            request.session.modified = True
            
            messages.success(request, 'Item removed from cart')
        
        return redirect('cart:cart')

class CheckoutView(LoginRequiredMixin, View):
    def get(self, request):
        cart = request.session.get('cart', {})
        
        if not cart:
            messages.error(request, 'Your cart is empty')
            return redirect('cart:cart')
        
        cart_items = []
        total_price = Decimal('0.00')
        
        for book_id, quantity in cart.items():
            book = get_object_or_404(Book, id=book_id)
            price = book.price * Decimal(quantity)
            total_price += price
            cart_items.append({
                'book': book,
                'quantity': quantity,
                'price': price,
            })
        
        context = {
            'cart_items': cart_items,
            'total_price': total_price,
        }
        return render(request, 'cart/checkout.html', context)
    
    def post(self, request):
        cart = request.session.get('cart', {})
        
        if not cart:
            messages.error(request, 'Your cart is empty')
            return redirect('cart:cart')
        
        # Get form data
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        phone = request.POST.get('phone')
        
        # Validation
        if not (full_name and email and address and city and postal_code and phone):
            messages.error(request, 'All fields are required')
            return redirect('cart:checkout')
        
        # Calculate total price
        total_price = Decimal('0.00')
        for book_id, quantity in cart.items():
            book = get_object_or_404(Book, id=book_id)
            total_price += book.price * Decimal(quantity)
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            email=email,
            address=address,
            city=city,
            postal_code=postal_code,
            phone=phone,
            total_price=total_price,
        )
        
        # Create order items and update stock
        for book_id, quantity in cart.items():
            book = get_object_or_404(Book, id=book_id)
            OrderItem.objects.create(
                order=order,
                book=book,
                price=book.price,
                quantity=quantity,
            )
            
            # Update stock
            book.stock -= quantity
            book.save()
        
        # Clear cart
        request.session['cart'] = {}
        request.session.modified = True
        
        # Redirect to order confirmation
        return redirect('cart:order_confirmation', order_id=order.id)

class OrderConfirmationView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        
        context = {
            'order': order,
        }
        return render(request, 'cart/order_confirmation.html', context)
    
class ClearCartView(View):
    def post(self, request):
        request.session['cart'] = {}
        request.session.modified = True
        messages.success(request, 'Cart cleared successfully')
        return redirect('cart:cart')