from django.shortcuts import render, redirect
from .models import Product, Category
from django.db.models.aggregates import Count

def render_products_home(request):
	context = {
		'products': Product.objects.all(),
		'categories': Category.objects.all().annotate(len=Count('id')),
		'page': 'All'
	}
	return render(request, 'products_home.html', context)

def render_product_page(request, id):
	context = {
		'product': Product.objects.get(id=id),
		'similar_items': Product.objects.filter(category=Product.objects.get(id=id).category)
	}
	return render(request, 'product_page.html', context)

def render_category_page(request, name):
	context = {
		'products': Product.objects.filter(category_id=Category.objects.get(name=name).id),
		'categories': Category.objects.all().annotate(len=Count('id')),
		'page': name
	}
	return render(request, 'products_home.html', context)

def search_products(request):
	context = {
		'categories': Category.objects.all().annotate(len=Count('id'))
	}
	print('hi')
	if (request.GET['search'] == ""):
		context['products'] = Product.objects.all()
	else:
		context['products'] = Product.objects.filter(name=request.GET['search'])
	return render(request, 'products_home.html', context)