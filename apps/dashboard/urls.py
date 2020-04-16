from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.render_dashboard),
    path('logout', views.logout),
    path('products', views.render_product_dashboard),
    path('add_product', views.add_product),
    path('ajax/delete_product', views.delete_product),
    path('products/', views.search_products),
]