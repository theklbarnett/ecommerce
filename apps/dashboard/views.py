from django.shortcuts import render, redirect
from apps.products.models import Product, Category
from django.http import JsonResponse

def render_dashboard(request):
	return render(request, 'order_dashboard.html')

def render_product_dashboard(request):
	context = {
		'products': Product.objects.all(),
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