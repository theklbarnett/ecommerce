from django.shortcuts import render, redirect
from .models import Product, Category
from django.db.models.aggregates import Count

def render_products_home(request):
	context = {
		'products': Product.objects.all(),
		'categories': Category.objects.all().annotate(len=Count('products')),
		'page': 'All'
	}
	return render(request, 'products_home.html', context)

def render_product_page(request, id):
	context = {
		'product': Product.objects.get(id=id),
		'similar_items': Product.objects.filter(category=Product.objects.get(id=id).category).exclude(id=id)
	}
	return render(request, 'product_page.html', context)

def render_category_page(request, name):
	context = {
		'products': Product.objects.filter(category_id=Category.objects.get(name=name).id),
		'categories': Category.objects.all().annotate(len=Count('id')),
		'page': name
	}
	return render(request, 'products_home.html', context)

def render_shopping_cart(request):
	return render(request, 'shopping_cart.html')

def add_to_cart(request):
	if request.session.get(Product.objects.get(id=request.POST['id']).name, False):
		request.session[Product.objects.get(id=request.POST['id']).name] += int(request.POST['quantity'])
	else:
		request.session[Product.objects.get(id=request.POST['id']).name] = int(request.POST['quantity'])
	if request.session.get('total_items', False):
		request.session['total_items'] += int(request.POST['quantity'])
	else: 
		request.session['total_items'] = int(request.POST['quantity'])
	return redirect('/products')


def search_products(request):
	context = {
		'categories': Category.objects.all().annotate(len=Count('id'))
	}
	if (request.GET['search'] == ""):
		context['products'] = Product.objects.all()
	else:
		context['products'] = Product.objects.filter(name=request.GET['search'])
	return render(request, 'products_home.html', context)