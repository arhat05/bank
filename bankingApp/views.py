from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def dashboard(request):
    return render(request, 'bankingApp/index.html')

def signup(request):
    return render(request, 'bankingApp/signup.html')

def login(request):
    return render(request, 'bankingApp/login.html')

def signout(request):
    pass
