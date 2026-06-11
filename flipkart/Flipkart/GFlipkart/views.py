from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Product, Cart, CartItem, Order, OrderItem
from .forms import RegisterForm, LoginForm, CheckoutForm

# Home Page - Display all products
# optional path parameter `category` lets us have URLs like /category/mobile/
def home(request, category=None):
    # prefer explicit path parameter, otherwise fall back to querystring
    if category is None:
        category = request.GET.get('category')

    if category:
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()

    # build list of categories for button links
    categories = [choice[0] for choice in Product.CATEGORY_CHOICES]

    context = {
        'products': products,
        'categories': categories,
        'selected_category': category,
    }
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            context['cart_items'] = cart.get_item_count()
        except Cart.DoesNotExist:
            context['cart_items'] = 0
    return render(request, 'home.html', context)

# User Registration
def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Cart.objects.create(user=user)
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form})

# User Login
def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

# User Logout
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')

# Add Product to Cart
@login_required(login_url='login')
@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    quantity = int(request.POST.get('quantity', 1))
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    messages.success(request, f'{product.name} added to cart!')
    return redirect('home')

# View Cart
@login_required(login_url='login')
def view_cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.cartitem_set.all()
        total = cart.get_total()
    except Cart.DoesNotExist:
        cart_items = []
        total = 0
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'cart.html', context)

# Update Cart Item Quantity
@login_required(login_url='login')
@require_POST
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity <= 0:
        cart_item.delete()
        messages.info(request, 'Item removed from cart.')
    else:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, 'Cart updated.')
    
    return redirect('view_cart')

# Remove Item from Cart
@login_required(login_url='login')
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.info(request, f'{product_name} removed from cart.')
    return redirect('view_cart')

# Checkout Page
@login_required(login_url='login')
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.cartitem_set.all()
        total = cart.get_total()
    except Cart.DoesNotExist:
        messages.error(request, 'Your cart is empty!')
        return redirect('home')
    
    if not cart_items:
        messages.error(request, 'Your cart is empty!')
        return redirect('home')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            shipping_address = form.cleaned_data['shipping_address']
            city = form.cleaned_data['city']
            postal_code = form.cleaned_data['postal_code']
            country = form.cleaned_data['country']
            
            full_address = f"{shipping_address}, {city}, {postal_code}, {country}"
            
            # Create Order
            order = Order.objects.create(
                user=request.user,
                total_amount=total,
                shipping_address=full_address
            )
            
            # Create Order Items
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            
            # Clear Cart
            cart.cartitem_set.all().delete()
            
            messages.success(request, 'Order placed successfully!')
            return redirect('order_confirmation', order_id=order.id)
    else:
        form = CheckoutForm()
    
    context = {
        'form': form,
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'checkout.html', context)

# Order Confirmation
@login_required(login_url='login')
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.items.all()
    
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'order_confirmation.html', context)

# Order History
@login_required(login_url='login')
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    context = {
        'orders': orders,
    }
    return render(request, 'order_history.html', context)

# Order Detail
@login_required(login_url='login')
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.items.all()
    
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'order_detail.html', context)
