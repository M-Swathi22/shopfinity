from django.shortcuts import render

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

def cart(request):
    return render(request, 'cart.html')

def wishlist(request):
    return render(request, 'wishlist.html')

def categories(request):
    return render(request, 'categories.html')


def category_products(request, category_name):
    return render(request, 'category_products.html', {'category': category_name})

# Create your views here.
