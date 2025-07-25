from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def register(request):
    return render(request, 'register.html')

def login_view(request):
    return render(request, 'login.html')

def cart(request):
    return render(request, 'cart.html')

def wishlist(request):
    return render(request, 'wishlist.html')



# Create your views here.
