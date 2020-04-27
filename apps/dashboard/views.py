from django.shortcuts import render, redirect
from apps.products.models import Product, Category
from .models import Order, Quantity, CustomerBilling, CustomerShipping
from django.http import JsonResponse
from django.db.models import Q, F, ExpressionWrapper, FloatField, Sum

def render_dashboard(request):
	context = {
		'orders': Order.objects.all()
	}
	return render(request, 'order_dashboard.html', context)

def render_product_dashboard(request):
	context = {
		'products': Product.objects.all().annotate(sold=Sum('quantity__number')),
		'categories': Category.objects.all()
	}
	return render(request, 'product_dashboard.html', context)

def search_products(request):
	context = {}
	if (request.GET['search'] == ""):
		context['products'] = Product.objects.all()
	else:
		context['products'] = Product.objects.filter(name=request.GET['search'])
	return render(request, 'product_dashboard.html', context)

def add_product(request):
	#validation
	if request.method == 'POST':
		if request.POST.get('new_category', False):
			Category.objects.create(name=request.POST['new_category'])
			Product.objects.create(name=request.POST['name'], description=request.POST['description'], price=request.POST['price'], category_id=Category.objects.get(name=request.POST['new_category']).id, stock_photo=request.FILES['img'])
		else:
			Product.objects.create(name=request.POST['name'], description=request.POST['description'], price=request.POST['price'], category_id=request.POST['category'], stock_photo=request.FILES['img'])
	return redirect('/dashboard/products')

def delete_product(request):
	data = {}
	if request.GET.get('product_id', None) != None:
		product_id = request.GET.get('product_id', None)
		Product.objects.get(id=product_id).delete()
		data['deleted'] = True
	return JsonResponse(data)

def logout(request):
	request.session.flush()
	return redirect('/admin')

#This is structured for some sort of prevention from random get requests to be implemented
def change_status(request):
	data = {
		'success': False
	}
	c = Order.objects.get(id=request.GET['order_id'])
	c.status = request.GET['newstatus'].replace('-', ' ')
	c.save()
	data['success'] = True
	return JsonResponse(data)

def filter_orders(request):
	context = {}
	if request.GET['status'].replace('-', ' ') == 'Show All':
		context['orders'] = Order.objects.all()
	else:
		context['orders'] = Order.objects.filter(status=request.GET['status'].replace('-', ' '))
	return render(request, 'order_table.html', context)

def search_orders(request):
	context = {}
	if (request.GET['search'] == ""):
		context['orders'] = Order.objects.all()
	else:
		context['orders'] = Order.objects.filter(Q(id__icontains=request.GET['search']) | Q(created_at__icontains=request.GET['search']) | Q(billing__first_name__icontains=request.GET['search']) | Q(billing__last_name__icontains=request.GET['search']) | Q(billing__address__icontains=request.GET['search']) |  Q(billing__city__icontains=request.GET['search']) | Q(billing__state__icontains=request.GET['search']) | Q(billing__zipcode__icontains=request.GET['search']))
	return render(request, 'order_dashboard.html', context)

def render_order_page(request, id):
	context = {
		'order': Order.objects.get(id=id),
		'products': Product.objects.filter(orders__id=id).annotate(quant=F('quantity__number'), quantprice=(ExpressionWrapper(F('quantity__number')*F('price'), output_field=FloatField()))),
	}
	return render(request, 'order_page.html', context)

def render_edit_product(request):
	context = {
		'product': Product.objects.get(id=request.GET['product-id']),
		'categories': Category.objects.all()
	}
	return render(request, 'edit_product_form.html', context)

def edit_product(request):
	if request.method == 'POST':
		p = Product.objects.get(id=request.POST['product_id'])
		p.name = request.POST['name']
		p.price = request.POST['price']
		p.description = request.POST['description']
		p.category = Category.objects.get(id=request.POST['category'])
		p.save()
	return redirect('/dashboard/products')
