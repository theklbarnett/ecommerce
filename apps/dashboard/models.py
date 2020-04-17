from django.db import models
from apps.products.models import Product

class CustomerShipping(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class CustomerBilling(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Order(models.Model):
	products = models.ManyToManyField(Product, related_name='orders')
	subtotal = models.DecimalField(decimal_places=2, max_digits=7)
	shipping = models.ForeignKey(CustomerShipping, related_name='orders', on_delete = models.CASCADE)
	billing =models.ForeignKey(CustomerBilling, related_name='orders', on_delete = models.CASCADE)
	status = models.CharField(max_length=60)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)