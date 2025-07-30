from django.shortcuts import render,redirect,get_object_or_404
from .models import Product,Category,Cart
from django.http import Http404



def base(request):
    return render(request,'base.html')

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(name, email, password)
    return render(request, 'register.html')

def login_view(request):
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
    print("Add to Cart view triggered")
    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:  # ✅ FIXED: check with string key
        cart[product_id_str] += 1
    else:
        cart[product_id_str] = 1

    request.session['cart'] = cart
    request.session.modified = True
    print("Cart contents:", request.session.get('cart'))
    return redirect('view_cart')


def cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))  # convert str to int
            item_total = product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total_price': item_total
            })
            total += item_total
        except Product.DoesNotExist:
            continue

    context = {
        'cart_items': cart_items,
        'total': total
    }
    print("Cart items in view:",cart_items)
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

