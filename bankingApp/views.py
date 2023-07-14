from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Customer
from django.contrib import messages
import time
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login

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
            
            user = User.objects.create_user(username=username, password=password1)
            user.email = email
            user.first_name = firstname
            user.last_name = lastname
            
            user.save()
            
            
            messages.success(request, "Account created successfully! Login to continue.")
            
            time.sleep(2)
            
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'bankingApp/signup.html')
        
        
        
    return render(request, 'bankingApp/signup.html')



def login(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        
        
        if user is not None:
            auth_login(request, user)
            name = user.first_name + "!"
            
            return render(request, 'bankingApp/index.html', {'name': name})
        
        else:
            messages.error(request, 'Invalid credentials!')
            return redirect('dahsboard')
    
    return render(request, 'bankingApp/login.html')

def signout(request):
    pass
