from django.db import models

class Category(models.Model):
	name = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Product(models.Model):
	price = models.DecimalField(decimal_places=2, max_digits=7)
	name = models.CharField(max_length=255)
	description = models.TextField()
	category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
	stock_photo = models.ImageField()
	inventory = models.IntegerField(default=100)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)