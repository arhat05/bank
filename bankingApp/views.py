from datetime import timezone
import datetime
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import *
from django.contrib import messages
import time
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.core.paginator import Paginator
from decimal import Decimal
from itertools import chain

# Create your views here.

def dashboard(request):
    
    if request.user.is_authenticated:
        first_name = request.user.first_name
            
        checking_acc = Account.objects.get(account_type="checking", customer_id=(Customer.objects.get(username=request.user.username)).customer_id)
        savings_acc = Account.objects.get(account_type="savings", customer_id=(Customer.objects.get(username=request.user.username)).customer_id)
        cc_acc = Account.objects.get(account_type="credit_card", customer_id=(Customer.objects.get(username=request.user.username)).customer_id)
        loan_acc = Account.objects.get(account_type="loan", customer_id=(Customer.objects.get(username=request.user.username)).customer_id)
        
        
        checking_account_num = checking_acc.account_number
        checking_transactions = Check.objects.filter(account_number=checking_account_num, transaction_type = "debit").values('transaction_amount', 'transaction_desc')
        checking_account_balance = checking_acc.balance
        
        # running_balance = 0
        
        # for transaction in checking_transactions:
        #     if transaction.transaction_type == 'credit':
        #         running_balance += transaction.transaction_amount
        #     elif transaction.transaction_type == 'debit':
        #         running_balance -= transaction.transaction_amount
        
        # checking_acc.balance = running_balance
        # checking_acc.save()
        
        

        
                
        savings_account_num = savings_acc.account_number
        savings_account_balance = savings_acc.balance
        savings_transactions = Saving.objects.filter(account_number=savings_account_num, transaction_type = "debit").values('transaction_amount', 'transaction_desc')
        
        
        
        
        # running_balance = 0
        
        # for transaction in savings_transactions:
        #     if transaction.transaction_type == 'credit':
        #         savings_account_balance += transaction.transaction_amount
        #     elif transaction.transaction_type == 'debit':
        #         savings_account_balance -= transaction.transaction_amount
        
        
        cc_acc_num = cc_acc.account_number
        cc_transactions = CreditCard.objects.filter(account_number=cc_acc_num, transaction_type = "credit").values('transaction_amount', 'transaction_desc')
        

        
        # get top 2 transaction categories by amount spent in the last 30 days for all accounts
        transactions = chain(checking_transactions, savings_transactions, cc_transactions)
        amount_spent = {}
        for transaction in transactions:
            if transaction['transaction_desc'] in amount_spent:
                amount_spent[transaction['transaction_desc']] += transaction['transaction_amount']
            else:
                amount_spent[transaction['transaction_desc']] = transaction['transaction_amount']
        
        # sort the dictionary by value (amount spent) in descending order
        amount_spent = dict(sorted(amount_spent.items(), key=lambda item: item[1], reverse=True))
        
        top2 = []
        
        if (amount_spent):
            if len(amount_spent) >= 2 and list(amount_spent.keys())[0] != 'other' and list(amount_spent.keys())[1] != 'other':
                top2.append(list(amount_spent.keys())[0])
                top2.append(list(amount_spent.keys())[1])
            elif len(amount_spent) >= 2 and list(amount_spent.keys())[0] == 'other':
                top2.append(list(amount_spent.keys())[1])
                top2.append(list(amount_spent.keys())[2])
            elif len(amount_spent) > 2 and list(amount_spent.keys())[1] == 'other':
                top2.append(list(amount_spent.keys())[0])
                top2.append(list(amount_spent.keys())[2])
            elif len (amount_spent) == 1 and list(amount_spent.keys())[0] != 'other':
                top2.append(list(amount_spent.keys())[0])
            else:
                top2.append(list(amount_spent.keys())[0])
                
                
                
                
        if top2:
            if len(top2) == 1:
                promos = Promotion.objects.filter(promotion_desc = top2[0])
            else:
                promos = Promotion.objects.filter(promotion_desc = top2[0]) | Promotion.objects.filter(promotion_desc = top2[1])
           
        # print(amount_spent) 
        # print(top2)
        # print(promos)
        
        return render(request, 'bankingApp/index.html', {
            'first_name': first_name,
            'checking_account_num': checking_account_num,
            'checking_account_balance': checking_account_balance,
            'savings_account_num': savings_acc.account_number,
            'savings_account_balance': savings_acc.balance,
            'cc_account_num': cc_acc.account_number,
            'cc_account_balance': cc_acc.balance,
            'loan_account_num': loan_acc.account_number,
            'loan_account_balance': loan_acc.balance,
            'promos': promos
        })
        
    
    return render(request, 'bankingApp/index.html')

def signup(request):
    
    if request.method == 'POST':
        
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password']
        confirm_password = request.POST['confirmpassword']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('signup')
        
        if password1 == confirm_password:
            
            customer = Customer(
            firstname=firstname,
            lastname=lastname,
            email=email,
            username=username,
            password=password1)

            customer.save()
            
            # create 4 accounts for the customer of each type
          
            account1 = Account(account_type="checking", customer_id=customer)
            account1.save()
            
            account2 = Account(account_type="savings", customer_id=customer)
            account2.save()
            
            account3 = Account(account_type="credit_card", customer_id=customer, interest_rate=20.5, credit_limit=1000)
            account3.save()
            
            account4 = Account(account_type="loan", customer_id=customer, interest_rate=19)
            account4.save()
            
            user = User.objects.create_user(username=username, password=password1)
            user.email = email
            user.first_name = firstname
            user.last_name = lastname
            #user.id = customer.customer_id
            
            # user.checking_account_num = Account.objects.get(account_type="checking", customer_id=customer.customer_id).account_number
            # user.checking_account_balance = Account.objects.get(account_type="checking", customer_id=customer.customer_id).balance
            # user.savings_account_num = Account.objects.get(account_type="savings", customer_id=customer.customer_id).account_number
            # user.savings_account_balance = Account.objects.get(account_type="savings", customer_id=customer.customer_id).balance
            
            
            user.save()
            
            
            messages.success(request, "Account created successfully!")
            
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
            customer = Customer.objects.get(username=username)
            auth_login(request, user)
            first_name = user.first_name
            
            checking_acc = Account.objects.get(account_type="checking", customer_id=customer.customer_id)
            savings_acc = Account.objects.get(account_type="savings", customer_id=customer.customer_id)
            cc_acc = Account.objects.get(account_type="credit_card", customer_id=customer.customer_id)
            loan_acc = Account.objects.get(account_type="loan", customer_id=customer.customer_id)
            
            
            checking_account_num = checking_acc.account_number
            checking_account_balance = checking_acc.balance
            checking_transactions = Check.objects.filter(account_number=checking_account_num)
            
            
            running_balance = 0
            
            for transaction in checking_transactions:
                if transaction.transaction_type == 'credit':
                    running_balance += transaction.transaction_amount
                elif transaction.transaction_type == 'debit':
                    running_balance -= transaction.transaction_amount
            
            checking_acc.balance = running_balance
            checking_acc.save()
                    
            savings_account_num = savings_acc.account_number
            savings_account_balance = savings_acc.balance
            savings_transactions = Saving.objects.filter(account_number=savings_account_num)
            
            running_balance = 0
            
            for transaction in savings_transactions:
                if transaction.transaction_type == 'credit':
                    running_balance += transaction.transaction_amount
                elif transaction.transaction_type == 'debit':
                    running_balance -= transaction.transaction_amount
            
            savings_acc.balance = running_balance
            savings_acc.save()
            
            cc_acc_num = cc_acc.account_number
            cc_acc_balance = cc_acc.balance
            cc_transactions = CreditCard.objects.filter(account_number=cc_acc_num)
            
            running_balance = 0
            
            for transaction in cc_transactions:
                if transaction.transaction_type == 'credit':
                    running_balance -= transaction.transaction_amount
                elif transaction.transaction_type == 'debit':
                    running_balance += transaction.transaction_amount
            
            cc_acc.balance = running_balance
            cc_acc.save()
            
            
            loan_acc_num = loan_acc.account_number
            loan_acc_balance = loan_acc.balance
            loan_transactions = Loan.objects.filter(account_number=loan_acc_num)
            
            running_balance = 0
            
            for transaction in loan_transactions:
                if transaction.transaction_type == 'credit':
                    running_balance += transaction.transaction_amount
                elif transaction.transaction_type == 'debit':
                    running_balance -= transaction.transaction_amount
            
            loan_acc.balance = running_balance
            loan_acc.save()
            
            total_transactions = chain((Check.objects.filter(account_number=checking_account_num, transaction_type = "debit").values('transaction_amount', 'transaction_desc')), 
                                       (Saving.objects.filter(account_number=savings_account_num, transaction_type = "debit").values('transaction_amount', 'transaction_desc')), 
                                       (CreditCard.objects.filter(account_number=cc_acc_num, transaction_type = "credit").values('transaction_amount', 'transaction_desc')))
            
            amount_spent = {}
            for transaction in total_transactions:
                if transaction['transaction_desc'] in amount_spent:
                    amount_spent[transaction['transaction_desc']] += transaction['transaction_amount']
                else:
                    amount_spent[transaction['transaction_desc']] = transaction['transaction_amount']
            
            # sort the dictionary by value (amount spent) in descending order
            amount_spent = dict(sorted(amount_spent.items(), key=lambda item: item[1], reverse=True))
            
            top2 = []
            
            if (amount_spent):
                if len(amount_spent) >= 2 and list(amount_spent.keys())[0] != 'other' and list(amount_spent.keys())[1] != 'other':
                    top2.append(list(amount_spent.keys())[0])
                    top2.append(list(amount_spent.keys())[1])
                elif len(amount_spent) >= 2 and list(amount_spent.keys())[0] == 'other':
                    top2.append(list(amount_spent.keys())[1])
                    top2.append(list(amount_spent.keys())[2])
                elif len(amount_spent) > 2 and list(amount_spent.keys())[1] == 'other':
                    top2.append(list(amount_spent.keys())[0])
                    top2.append(list(amount_spent.keys())[2])
                elif len (amount_spent) == 1 and list(amount_spent.keys())[0] != 'other':
                    top2.append(list(amount_spent.keys())[0])
                else:
                    top2.append(list(amount_spent.keys())[0])
                    
                    
            if top2:
                if len(top2) == 1:
                    promos = Promotion.objects.filter(promotion_desc = top2[0])
                else:
                    promos = Promotion.objects.filter(promotion_desc = top2[0]) | Promotion.objects.filter(promotion_desc = top2[1])
            
            
            return render(request, 'bankingApp/index.html', {
                'first_name': first_name,
                'checking_account_num': checking_account_num,
                'checking_account_balance': checking_account_balance,
                'savings_account_num': savings_account_num,
                'savings_account_balance': savings_account_balance,
                'cc_account_num': cc_acc_num,
                'cc_account_balance': cc_acc_balance,
                'loan_account_num': loan_acc_num,
                'loan_account_balance': loan_acc_balance,
                'promos': promos
            })

        else:
            messages.error(request, 'Invalid credentials!')
            return redirect('dashboard')
    
    return render(request, 'bankingApp/login.html')

def signout(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('dashboard')


def checkingaccount(request):
    account = Account.objects.get(account_type="checking", customer_id=(Customer.objects.get(username=request.user.username)).customer_id)
    accNum = account.account_number
    transactions = Check.objects.filter(account_number=accNum).order_by('-transaction_date')
    
    #set the account balance to the sum of all transactions and the initial balance
    
    balance = 0
    for transaction in transactions:
        if transaction.transaction_type == 'credit':
            balance += transaction.transaction_amount
        elif transaction.transaction_type == 'debit':
            balance -= transaction.transaction_amount
            
    account.balance = balance
    account.save()
    
    
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Convert the start and end dates to Python date objects
    if start_date:
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    if end_date:
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

    # Apply date filtering if start_date and end_date are valid
    if start_date and end_date:
        transactions = transactions.filter(transaction_date__range=[start_date, end_date])
    elif start_date:
        transactions = transactions.filter(transaction_date__gte=start_date)
    elif end_date:
        transactions = transactions.filter(transaction_date__lte=end_date)
    
    
    # paginate transactions 25 per page
    paginator = Paginator(transactions, 25) 

    # get current page number
    page = request.GET.get('page')
    transactions = paginator.get_page(page)
    
    

    return render(request, 'bankingApp/checkingaccount.html', {'account': account, 'transactions': transactions})

def savingsaccount(request):
    account = Account.objects.get(account_type="savings", customer_id=(Customer.objects.get(username=request.user.username)).customer_id)
    accNum = account.account_number
    transactions = Saving.objects.filter(account_number=accNum).order_by('-transaction_date')
    
    #set the account balance to the sum of all transactions and the initial balance
    
    balance = 0
    #interest = balance * account.interest_rate/100
    for transaction in transactions:
        if transaction.transaction_type == 'credit':
            balance += transaction.transaction_amount
        elif transaction.transaction_type == 'debit':
            balance -= transaction.transaction_amount
    
    
    #balance += interest
    account.balance = balance
    
    
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Convert the start and end dates to Python date objects
    if start_date:
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    if end_date:
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

    # Apply date filtering if start_date and end_date are valid
    if start_date and end_date:
        transactions = transactions.filter(transaction_date__range=[start_date, end_date])
    elif start_date:
        transactions = transactions.filter(transaction_date__gte=start_date)
    elif end_date:
        transactions = transactions.filter(transaction_date__lte=end_date)
    
    
    # paginate transactions 25 per page
    paginator = Paginator(transactions, 25) 

    # get current page number
    page = request.GET.get('page')
    transactions = paginator.get_page(page)
    

    return render(request, 'bankingApp/savingsaccount.html', {'account': account, 'transactions': transactions})

def creditcard(request):
    account = Account.objects.get(account_type="credit_card", customer_id=(Customer.objects.get(username=request.user.username)).customer_id)
    accNum = account.account_number
    transactions = CreditCard.objects.filter(account_number=accNum).order_by('-transaction_date')
    
    #set the account balance to the sum of all transactions and the initial balance
    
    balance = 0
    for transaction in transactions:
        if transaction.transaction_type == 'credit':
            balance += transaction.transaction_amount
        elif transaction.transaction_type == 'debit':
            balance -= transaction.transaction_amount
            
    
    account.balance = balance
    
    account.save()
    
    
        
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Convert the start and end dates to Python date objects
    if start_date:
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    if end_date:
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

    # Apply date filtering if start_date and end_date are valid
    if start_date and end_date:
        transactions = transactions.filter(transaction_date__range=[start_date, end_date])
    elif start_date:
        transactions = transactions.filter(transaction_date__gte=start_date)
    elif end_date:
        transactions = transactions.filter(transaction_date__lte=end_date)
    
    
    # paginate transactions 25 per page
    paginator = Paginator(transactions, 25) 

    # get current page number
    page = request.GET.get('page')
    transactions = paginator.get_page(page)

    return render(request, 'bankingApp/creditcard.html', {'account': account, 'transactions': transactions})

def loan(request):
    
    account = Account.objects.get(account_type="loan", customer_id=(Customer.objects.get(username=request.user.username)).customer_id)
    accNum = account.account_number
    transactions = CreditCard.objects.filter(account_number=accNum).order_by('-transaction_date')
    
    #set the account balance to the sum of all transactions and the initial balance
    
    balance = account.balance
    for transaction in transactions:
        if transaction.transaction_type == 'credit':
            balance -= transaction.transaction_amount
        elif transaction.transaction_type == 'debit':
            balance += transaction.transaction_amount
            
    
    account.balance = balance
    
    account.save()
    
    
        
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Convert the start and end dates to Python date objects
    if start_date:
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    if end_date:
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

    # Apply date filtering if start_date and end_date are valid
    if start_date and end_date:
        transactions = transactions.filter(transaction_date__range=[start_date, end_date])
    elif start_date:
        transactions = transactions.filter(transaction_date__gte=start_date)
    elif end_date:
        transactions = transactions.filter(transaction_date__lte=end_date)
    
    
    # paginate transactions 25 per page
    paginator = Paginator(transactions, 25) 

    # get current page number
    page = request.GET.get('page')
    transactions = paginator.get_page(page)

    return render(request, 'bankingApp/loan.html', {'account': account, 'transactions': transactions})

def make_transaction(request):
    if request.method == 'POST':
        # Get the form data from the request
        transaction_amount = Decimal(request.POST['transaction_amount'])
        transaction_date = datetime.datetime.strptime(request.POST['transaction_date'], '%Y-%m-%d').date()
        transaction_desc = request.POST['transaction_description']
        transaction_type = request.POST['transaction_type']
        account_type = request.POST['account_type']
        
        
        account = Account.objects.get(account_type=account_type, customer_id=(Customer.objects.get(username=request.user.username)).customer_id)
        #account = Account.objects.get(account_type="checking", customer_id=(Customer.objects.get(username=request.user.username)).customer_id)
        
        if account_type == 'checking':
        # Create a new transaction object and save it
            transaction = Check(account_number=account,
                                transaction_date=transaction_date,
                                transaction_desc=f"{transaction_desc}",
                                transaction_type=transaction_type,
                                transaction_amount=transaction_amount)
            transaction.save()
                    # Update the account balance based on the new transaction
            if transaction.transaction_type == 'credit':
                account.balance += transaction.transaction_amount
            elif transaction.transaction_type == 'debit':
                account.balance -= transaction.transaction_amount

            account.save()
            
        elif account_type == 'savings':
            transaction = Saving(account_number=account,
                                transaction_date=transaction_date,
                                transaction_desc=f"{transaction_desc}",
                                transaction_type=transaction_type,
                                transaction_amount=transaction_amount)
            transaction.save()
                    # Update the account balance based on the new transaction
            if transaction.transaction_type == 'credit':
                account.balance += transaction.transaction_amount
            elif transaction.transaction_type == 'debit':
                account.balance -= transaction.transaction_amount

            account.save()
        elif account_type == 'credit_card':
            
            if transaction_amount + account.balance > account.credit_limit and transaction_type == 'credit':
                messages.error(request, 'Transaction amount exceeds credit limit!')
                return redirect('creditcard')
            else: 
                transaction = CreditCard(account_number=account, 
                                        transaction_date=transaction_date,
                                        transaction_desc=f"{transaction_desc}",
                                        transaction_type=transaction_type,
                                        transaction_amount=transaction_amount)
                transaction.save()
                
                if transaction.transaction_type == 'credit':
                    account.balance -= transaction.transaction_amount
                elif transaction.transaction_type == 'debit':
                    account.balance += transaction.transaction_amount
                
                account.save()


        # Redirect back to the checking account page after the transaction is processed
        if account_type == 'checking':
            return redirect('checkingaccount')
        if account_type == 'savings':
            return redirect('savingsaccount')
        if account_type == 'credit_card':
            return redirect('creditcard')

    return render(request, 'bankingApp/make_transaction.html')