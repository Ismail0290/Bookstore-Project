from decimal import Decimal
from django.shortcuts import get_object_or_404
from books.models import Book

def cart_processor(request):
    # Get cart data safely with empty dict as default
    cart = request.session.get('cart', {})
    
    # Initialize values
    cart_count = 0
    cart_items = []
    total_price = Decimal('0.00')
    cleaned_cart = {}
    
    # Create a list of items to process (avoid modifying during iteration)
    items = list(cart.items())
    
    for book_id, quantity in items:
        try:
            # Handle case where quantity might be a dictionary
            if isinstance(quantity, dict):
                continue
                
            # Convert to integer safely
            quantity = int(quantity)
            if quantity <= 0:
                continue
                
            # Get book and calculate price
            book = get_object_or_404(Book, id=book_id)
            price = book.price * Decimal(quantity)
            
            # Update aggregates
            cart_count += quantity
            total_price += price
            cleaned_cart[str(book_id)] = quantity
            
            # Prepare cart items for templates
            cart_items.append({
                'book': book,
                'quantity': quantity,
                'price': price,
            })
            
        except (ValueError, TypeError, Book.DoesNotExist):
            continue
    
    # Update session with cleaned cart if changes were made
    if cleaned_cart != cart:
        request.session['cart'] = cleaned_cart
        request.session.modified = True
    
    return {
        'cart_count': cart_count,
        'cart_total': total_price,
        'cart_items': cart_items,
    }