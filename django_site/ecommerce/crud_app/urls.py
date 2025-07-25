from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('categories/', views.categories, name='categories'),
    path('categories/<str:category_name>/',views.category_products,name='category_products'),
    path('cart/', views.cart, name='cart'),
    path('wishlist/', views.wishlist, name='wishlist'),  
]

# Create your views here.
