from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Customer
from django.contrib import messages
import time

# Create your views here.

def dashboard(request):

    
    return render(request, 'bankingApp/index.html')

def signup(request):
    
    if request.method == 'POST':
        
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password']
        confirm_password = request.POST['confirmpassword']
        
        if password1 == confirm_password:
            customer = Customer(
            firstname=firstname,
            lastname=lastname,
            email=email,
            username=username,
            password=password1)

            customer.save()
            
            messages.success(request, 'Account created successfully! Login to continue.')
            
            time.sleep(5)
            
            return redirect('login')
        else:
            return messages.error(request, 'Passwords do not match!')
        
        
        
    return render(request, 'bankingApp/signup.html')


def login(request):
    return render(request, 'bankingApp/login.html')

def signout(request):
    pass
