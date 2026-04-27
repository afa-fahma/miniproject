from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('home/', views.product_list, name='home'),
    path('cart/', views.cart_view, name='cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    path('orders/', views.order_list, name='orders'),
    
   
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    
] 




