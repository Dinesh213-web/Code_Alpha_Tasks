from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Product, Order, OrderItem
from .forms import RegisterForm, LoginForm


# ─── Helpers ──────────────────────────────────────────────────────────────────

def get_cart(request):
    return request.session.get('cart', {})

def save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True


# ─── Product Views ─────────────────────────────────────────────────────────────

def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})


# ─── Cart Views ────────────────────────────────────────────────────────────────

def cart(request):
    cart = get_cart(request)
    cart_items = []
    total = 0
    for product_id, item in cart.items():
        try:
            product = Product.objects.get(pk=int(product_id))
            item_total = product.price * item['quantity']
            total += item_total
            cart_items.append({
                'product': product,
                'quantity': item['quantity'],
                'item_total': item_total,
            })
        except Product.DoesNotExist:
            pass
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total': total})


def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = get_cart(request)
    pid = str(pk)
    if pid in cart:
        cart[pid]['quantity'] += 1
    else:
        cart[pid] = {'quantity': 1, 'price': str(product.price)}
    save_cart(request, cart)
    messages.success(request, f'"{product.name}" added to cart!')
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def remove_from_cart(request, pk):
    cart = get_cart(request)
    pid = str(pk)
    if pid in cart:
        del cart[pid]
        save_cart(request, cart)
        messages.success(request, 'Item removed from cart.')
    return redirect('cart')


def update_cart(request, pk):
    if request.method == 'POST':
        cart = get_cart(request)
        pid = str(pk)
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0 and pid in cart:
            cart[pid]['quantity'] = quantity
            save_cart(request, cart)
            messages.success(request, 'Cart updated.')
        elif quantity == 0:
            return redirect('remove_from_cart', pk=pk)
    return redirect('cart')


# ─── Checkout & Orders ─────────────────────────────────────────────────────────

@login_required
def checkout(request):
    cart = get_cart(request)
    if not cart:
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart')

    if request.method == 'POST':
        order = Order.objects.create(user=request.user, status='completed')
        total = 0
        for product_id, item in cart.items():
            try:
                product = Product.objects.get(pk=int(product_id))
                qty = item['quantity']
                price = product.price
                OrderItem.objects.create(order=order, product=product, quantity=qty, price=price)
                total += price * qty
            except Product.DoesNotExist:
                pass
        order.total_price = total
        order.save()

        # Clear cart
        request.session['cart'] = {}
        request.session.modified = True

        messages.success(request, f'Order #{order.id} placed successfully! 🎉')
        return redirect('orders')

    # GET: show summary
    cart_items = []
    total = 0
    for product_id, item in cart.items():
        try:
            product = Product.objects.get(pk=int(product_id))
            item_total = product.price * item['quantity']
            total += item_total
            cart_items.append({'product': product, 'quantity': item['quantity'], 'item_total': item_total})
        except Product.DoesNotExist:
            pass
    return render(request, 'store/checkout.html', {'cart_items': cart_items, 'total': total})


@login_required
def orders(request):
    user_orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/orders.html', {'orders': user_orders})


# ─── Auth Views ────────────────────────────────────────────────────────────────

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f'Welcome, {user.username}! Account created.')
        return redirect('home')
    return render(request, 'store/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect(request.GET.get('next', 'home'))
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'store/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')
