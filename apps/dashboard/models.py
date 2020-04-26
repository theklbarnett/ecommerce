from django.db import models
from apps.products.models import Product

class CustomerShipping(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	address = models.CharField(max_length=255)
	address_2 = models.CharField(max_length=255)
	city = models.CharField(max_length=255)
	state = models.CharField(max_length=255)
	zipcode = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class CustomerBilling(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	address = models.CharField(max_length=255)
	address_2 = models.CharField(max_length=255)
	city = models.CharField(max_length=255)
	state = models.CharField(max_length=255)
	zipcode = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Order(models.Model):
	products = models.ManyToManyField(Product, related_name='orders')
	subtotal = models.DecimalField(decimal_places=2, max_digits=7)
	shipping = models.ForeignKey(CustomerShipping, related_name='orders', on_delete = models.CASCADE)
	billing = models.ForeignKey(CustomerBilling, related_name='orders', on_delete = models.CASCADE)
	status = models.CharField(max_length=60)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Quantity(models.Model):
	number = models.IntegerField()
	order = models.ForeignKey(Order, related_name='quantity', on_delete = models.CASCADE)
	product = models.ForeignKey(Product, related_name='quantity', on_delete = models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)