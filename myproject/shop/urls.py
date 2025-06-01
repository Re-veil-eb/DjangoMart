# shop/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('logout/', views.logout_view, name='logout'),
    path('products/add/', views.add_product_view, name='add_product'),  # Add this URL
    path('product/<int:product_id>/add_to_cart/', views.add_to_cart, name='add_to_cart'),  # Added URL for add_to_cart
    path('product/<int:product_id>/add_to_wishlist/', views.add_to_wishlist, name='add_to_wishlist'),  # Added URL for add_to_wishlist
]
