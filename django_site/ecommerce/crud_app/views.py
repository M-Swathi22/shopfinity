from django.shortcuts import render,redirect,get_object_or_404
from .models import Product,Category,Cart
from django.http import Http404
from .models import Customer


def base(request):
    return render(request,'base.html')

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        Customer.objects.create(name=name, email=email, password=password)
        return redirect('login')
    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            customer = Customer.objects.get(email=email, password=password)
            request.session['customer_id'] = customer.id
            return redirect('home')
        except Customer.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid email or password'})
    return render(request, 'login.html')

def wishlist(request):
    return render(request, 'wishlist.html')

def categories(request):
    return render(request, 'categories.html')

def category_products(request, category):
    try:
        category_obj = Category.objects.get(name__iexact=category)
    except Category.DoesNotExist:
        raise Http404("Category not found")

    products = Product.objects.filter(category=category_obj)

    return render(request, 'category_products.html', {
        'products': products,
        'category': category_obj.name,
    })

def product_detail(request, product_id):
    try:

        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        raise Http404("Product not found")
    
    return render(request, 'product_detail.html', {'product': product})

def add_to_cart(request, product_id):
    if 'customer_id' not in request.session:
        return redirect('login')  # Redirect to login if not logged in

    customer_id = request.session['customer_id']
    customer = Customer.objects.get(id=customer_id)
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = Cart.objects.get_or_create(
        customer=customer,
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('view_cart')

def cart(request):
    if 'customer_id' not in request.session:
        return redirect('login')  # Redirect if not logged in

    customer_id = request.session['customer_id']
    customer = Customer.objects.get(id=customer_id)

    cart_items_db = Cart.objects.filter(customer=customer)

    cart_items = []
    total = 0

    for item in cart_items_db:
        item_total = item.product.price * item.quantity
        cart_items.append({
            'product': item.product,
            'quantity': item.quantity,
            'total_price': item_total
        })
        total += item_total

    context = {
        'cart_items': cart_items,
        'total': total
    }

    print("Cart items from DB:", cart_items)
    return render(request, 'cart.html', context)


def place_order(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('view_cart')

    cart_items = []
    total = 0
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
            total += product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total_price': product.price * quantity
            })
        except Product.DoesNotExist:
            continue

    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'place_order.html', context)

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        del cart[product_id_str]
        request.session['cart'] = cart

    return redirect('view_cart')

from django.contrib import messages

def confirm_order(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "Your cart is empty.")
            return redirect('view_cart')

        # You can save order to DB later here
        request.session['cart'] = {}  # Clear the cart
        messages.success(request, "Order placed successfully!")
        return redirect('home')
    else:
        return redirect('view_cart')

