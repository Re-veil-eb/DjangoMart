# shop/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, Wishlist, Order
import stripe
from .models import Product, Category

from .forms import ProductForm
from django.contrib.admin.views.decorators import staff_member_required  # Only admin users can add products

# View to add products
@staff_member_required  # Restrict to staff (admin) users
def add_product_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # Include request.FILES to handle image upload
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Redirect to product list after adding a product
    else:
        form = ProductForm()
    
    return render(request, 'shop/add_product.html', {'form': form})

def product_list(request):
    category_id = request.GET.get('category')
    products = Product.objects.all()

    if category_id:
        products = products.filter(category_id=category_id)

    categories = Category.objects.all()  # For populating the dropdown

    return render(request, 'shop/product_list.html', {
        'products': products,
        'categories': categories
    })
# Set your Stripe secret key
stripe.api_key = 'your-stripe-secret-key'  # Replace with your actual Stripe secret key


from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('home') 

# User login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home or another view after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'shop/login.html', {'form': form})

# Home page view
def home(request):
    products = Product.objects.all()
    
    # Filter logic for category
    category = request.GET.get('category')
    if category:
        products = products.filter(category=category)
    
    # Price range filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price and max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)
    
    # Search query
    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)
    
    return render(request, 'shop/index.html', {'products': products})

# User registration view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'shop/register.html', {'form': form})

# Wishlist view
@login_required
def wishlist_view(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    products = wishlist.products.all()
    return render(request, 'shop/wishlist.html', {'products': products})

# Cart view
@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    products = cart.products.all()
    return render(request, 'shop/cart.html', {'products': products})

# Checkout view (with Stripe)
@login_required
def checkout_view(request):
    if request.method == 'POST':
        cart, created = Cart.objects.get_or_create(user=request.user)
        total = sum(product.price for product in cart.products.all())
        # Create a Stripe PaymentIntent
        intent = stripe.PaymentIntent.create(
            amount=int(total * 100),  # Convert dollars to cents
            currency='usd',
            metadata={'user_id': request.user.id}
        )
        return render(request, 'shop/checkout.html', {'client_secret': intent.client_secret})
    return redirect('cart')

# Add product to cart
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.products.add(product)
    return redirect('cart')

# Add product to wishlist
@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.add(product)
    return redirect('wishlist')

# Remove product from wishlist
@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist = get_object_or_404(Wishlist, user=request.user)
    wishlist.products.remove(product)
    return redirect('wishlist')

# Remove product from cart
@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_object_or_404(Cart, user=request.user)
    cart.products.remove(product)
    return redirect('cart')

