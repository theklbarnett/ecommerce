from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.render_signin),
    path('authenticate', views.authenticate_user),
]