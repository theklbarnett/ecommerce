from django.shortcuts import render, redirect
from .models import Admin
from django.contrib import messages
import bcrypt

def render_signin(request):
	if request.session.get('logged_on', False):
		return redirect('/dashboard')
	else:
		return render(request, 'admin_signin.html')

def authenticate_user(request):
	if request.method == "POST":
		errors = Admin.objects.authentication_validator(request.POST)
		if len(errors) > 0:
			for key, value in errors.items():
				messages.error(request, value, extra_tags='login')
			return redirect('/admin')
		else:
			request.session['first_name'] = Admin.objects.get(email=request.POST['email_login']).first_name
			request.session['logged_on'] = True
			request.session['user_id'] = Admin.objects.get(email=request.POST['email_login']).id
			return redirect('/dashboard')