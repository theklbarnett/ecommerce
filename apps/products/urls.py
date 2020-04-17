from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.render_products_home),
    path('show/<int:id>', views.render_product_page),
    path('category/<str:name>', views.render_category_page),
    path('search', views.search_products),
    path('cart', views.render_shopping_cart),
    path('add_to_cart', views.add_to_cart)
]