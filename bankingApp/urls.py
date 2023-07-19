from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('signout', views.signout, name='signout'),
    path('checkingaccount', views.checkingaccount, name='checkingaccount'),
    path('savingsaccount', views.savingsaccount, name='savingsaccount'),
    
]