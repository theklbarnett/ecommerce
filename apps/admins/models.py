from django.db import models
import re
import bcrypt

class AdminManager(models.Manager):
	def authentication_validator(self, post_data):
		errors = {}
		if Admin.objects.filter(email=post_data['email_login']):
			if not bcrypt.checkpw(post_data['password_login'].encode(), Admin.objects.get(email=post_data['email_login']).password_hash.encode()):
				errors['password'] = "Incorrect password"
		else:
			errors['email'] = 'This email does not exist'
		return errors

class Admin(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password_hash = models.CharField(max_length=60)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = AdminManager()