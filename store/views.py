
import stripe
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, Order
from .models import  CartItem
from django.conf import settings
from django.http import JsonResponse

stripe.api_key = settings.STRIPE_SECRET_KEY




# Show products
def product_list(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


# Add to cart
def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')

    product = Product.objects.get(id=product_id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


# View cart
def cart_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart_items = cart_items = Cart.objects.filter(user=request.user)

    total = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })
@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')

        # 🟢 CASH ON DELIVERY
        if payment_method == 'cod':
            for item in cart_items:
                Order.objects.create(
                    user=request.user,
                    product=item.product,
                    quantity=item.quantity,
                    total=item.product.price * item.quantity,
                    name=name,
                    phone=phone,
                    address=address,
                    payment_status="COD"
                )

            cart_items.delete()
            return redirect('success')

        # 🔵 ONLINE PAYMENT (Stripe)
        elif payment_method == 'online':
            request.session['name'] = name
            request.session['phone'] = phone
            request.session['address'] = address

            return redirect('create_checkout_session')

    return render(request, 'checkout.html', {
        'items': cart_items,
        'total': total
    })

def success(request):
    return render(request, 'success.html')
# def success(request):
#     Cart.objects.filter(user=request.user).delete()
#     return render(request, 'success.html')


def cancel(request):
    return render(request, 'cancel.html')


@login_required
def success(request):
    cart_items = Cart.objects.filter(user=request.user)

    name = request.session.get('name')
    phone = request.session.get('phone')
    address = request.session.get('address')

    for item in cart_items:
        Order.objects.create(
            user=request.user,
            product=item.product,
            quantity=item.quantity,
            total=item.product.price * item.quantity,
            name=name,
            phone=phone,
            address=address,
            payment_status="Paid"
        )

    cart_items.delete()

    return render(request, 'success.html')

def order_list(request):
    if not request.user.is_authenticated:
        return redirect('login')

    orders = Order.objects.filter(user=request.user).order_by('-ordered_at')

    return render(request, 'orders.html', {'orders': orders})

@login_required
def create_checkout_session(request):
    cart_items = Cart.objects.filter(user=request.user)

    line_items = []

    for item in cart_items:
        line_items.append({
            'price_data': {
                'currency': 'inr',
                'product_data': {
                    'name': item.product.name,
                },
                'unit_amount': int(item.product.price * 100),
            },
            'quantity': item.quantity,
        })

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri('/success/'),
        cancel_url=request.build_absolute_uri('/cancel/'),
    )

    return redirect(checkout_session.url, code=303)


    

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

# SIGNUP
def user_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.save()

        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'signup.html')


# LOGIN
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'login.html')


# LOGOUT
def user_logout(request):
    logout(request)
    return redirect('login')