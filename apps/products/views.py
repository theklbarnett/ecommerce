from django.shortcuts import render, redirect, HttpResponse
from .models import Product, Category
from django.db.models.aggregates import Count
from apps.dashboard.models import Order, CustomerShipping, CustomerBilling, Quantity

def render_products_home(request):
	#request.session.flush()
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
	if request.session.get('total_items', False):
		context = {
			'cart': Product.objects.filter(id__in=request.session['item_ids']),
			'total_price' : 0
		}
		for product in context['cart']:
			product.cart_quantity = request.session[str(product.id)]
			product.total = product.cart_quantity * product.price
			context['total_price'] += product.total
		request.session['checkout_total'] = str(context['total_price'])
		return render(request, 'shopping_cart.html', context)
	else:
		return redirect('/products')

def update_cart(request):
	if request.method == 'POST' and int(request.POST['quantity']) > 0:
		request.session['total_items'] += int(request.POST['quantity']) - request.session[request.POST['product_id']]
		request.session[request.POST['product_id']] = int(request.POST['quantity'])
	return redirect('/products/cart')

def delete_item(request, id):
	request.session['total_items'] -= int(request.session[id])
	request.session['item_ids'].remove(id)
	del request.session[id]
	request.session.modified = True
	return redirect('/products/cart')

def add_to_cart(request):
	if request.session.get(request.POST['id'], False):
		request.session[request.POST['id']] += int(request.POST['quantity'])
	else:
		request.session[request.POST['id']] = int(request.POST['quantity'])
	if request.session.get('total_items', False):
		request.session['total_items'] += int(request.POST['quantity'])
		request.session['item_ids'].append(request.POST['id'])
	else: 
		request.session['total_items'] = int(request.POST['quantity'])
		request.session['item_ids'] = [request.POST['id']]
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

# I am not attempting to do anything with the credit card information
# To actually charge the card I would incorporate paypal into the site by accessing
## their API
def checkout(request):
	if request.session.get('item_ids', False):
		newship = CustomerShipping.objects.create(first_name=request.POST['ship_first_name'], last_name=request.POST['ship_last_name'], address=request.POST['ship_address'], city=request.POST['ship_city'], state=request.POST['ship_state'], zipcode=int(request.POST['ship_zip']))
		if request.POST.get('ship_address_2', False):
			newship.address_2 = request.POST['ship_address_2']
			newship.save()
		newbill = CustomerBilling.objects.create(first_name=request.POST['bill_first_name'], last_name=request.POST['bill_last_name'], address=request.POST['bill_address'], city=request.POST['bill_city'], state=request.POST['bill_state'], zipcode=int(request.POST['bill_zip']))
		if request.POST.get('bill_address_2', False):
			newbill.address_2 = request.POST['bill_address_2']
			newbill.save()
		neworder = Order.objects.create(subtotal=float(request.session['checkout_total']), shipping=newship, billing=newbill, status="Order in process")
		for product in request.session['item_ids']:
			Quantity.objects.create(number=int(request.session[product]), product=Product.objects.get(id=int(product)), order=neworder)
			product.inventory -= int(request.session[product])
			product.save()
			neworder.products.add(Product.objects.get(id=int(product)))
		request.session.flush()

		return redirect(f'/products/checkout/order/{neworder.id}')
	else:
		return redirect('/products')

def order_confirmation(request, id):
	context = {
		'order': Order.objects.get(id=id)
	}
	return render(request, 'order_confirmation.html', context)


