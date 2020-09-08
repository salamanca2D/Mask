"""
URLS
"""
from django.urls import path

from . import views

urlpatterns = [
        #Leave as empty string for base url
	path('', views.inicio, name="inicio"),
	path('shop/', views.tienda, name="shop"),
	path('shop/<str:gender>', views.tienda, name="shop"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),

	path('update_item/', views.update_item, name="update_item"),
	path('process_order/', views.process_order, name="process_order"),

	path('get_item/', views.get_item, name="get_item"),
	path('set_opt/', views.set_opt, name="set_opt"),
]
