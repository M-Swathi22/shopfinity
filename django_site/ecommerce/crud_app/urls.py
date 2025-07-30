from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('categories/', views.categories, name='categories'),
    path('categories/<str:category>/', views.category_products, name='category_products'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='view_cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('wishlist/', views.wishlist, name='wishlist'), 
    path('place-order/', views.place_order, name='place_order'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('confirm-order/', views.confirm_order, name='confirm_order'),


]

# Create your views here.
