from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, UserLoginForm, CheckOutForm
from .models import Product, Cart, CartItem, Order, OrderItem
from django.contrib.auth import login, logout
from django.contrib import messages

def home_view(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('cart')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def product_list_view(request):
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 25)  # 25 products per page
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    return render(request, 'products.html', {'products': products})

def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('product')
    total = 0
    for item in items:
        item.subtotal = item.quantity * item.product.price
        total += item.subtotal
    return render(request, 'cart.html', {'items': items, 'total': total})

@login_required
def add_to_cart_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not item_created:
        item.quantity += 1
        item.save()
    return redirect('cart')

@login_required
def remove_from_cart_view(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('cart')

@login_required
def update_cart_quantity_view(request, item_id, action):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if action == "increase":
        item.quantity += 1
    elif action == "decrease" and item.quantity > 1:
        item.quantity -= 1
    item.save()
    return redirect('cart')

@login_required
def checkout_view(request):
    cart = Cart.objects.get(user=request.user)
    items = cart.items.select_related('product')
    total = 0
    for item in items:
        item.subtotal = item.product.price * item.quantity
        total += item.subtotal
    if not items:
        messages.warning(request, "Your cart is empty.")
        return redirect('cart')
    if request.method == 'POST':
        form = CheckOutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                address=form.cleaned_data['address']
            )
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            items.delete()
            messages.success(request, "Order placed successfully.")
            return redirect('order_success', order_id=order.id)
    else:
        form = CheckOutForm()
    return render(request, 'checkout.html', {
        'form': form,
        'items': items,
        'total': total
    })

@login_required
def order_success_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_success.html', {'order': order})

@login_required
def order_history_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-placed_at')
    return render(request, 'order_history.html', {'orders': orders})
