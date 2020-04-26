from django.urls import path, include
from . import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.render_dashboard),
    path('logout', views.logout),
    path('products', views.render_product_dashboard),
    path('add_product', views.add_product),
    path('ajax/delete_product', views.delete_product),
    path('products/', views.search_products),
    path('ajax/status_change', views.change_status),
    path('filter_orders', views.filter_orders, name='filter-orders'),
    path('search-orders', views.search_orders),
    path('orders', views.render_dashboard),
    path('orders/show/<int:id>', views.render_order_page)
]