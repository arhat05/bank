import datetime
from django.db import models

# Create your models here.

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField()
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    dob = models.DateField(null=True)
    phone = models.CharField(max_length=10, null=True)
    address = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=50, null=True)
    zipcode = models.CharField(max_length=6, null=True)
    ssn = models.CharField(max_length=9,  null=True)
    number_of_accounts = models.IntegerField(null=True)
    
class Account(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ('checking', 'Checking'),
        ('savings', 'Savings'),
        ('credit_card', 'Credit Card'),
        ('loan', 'Loan')
    ]

    account_number = models.AutoField(primary_key=True)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES, default='checking')
    date_opened = models.DateField(default=datetime.date.today)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)
    overdraft_lim = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    interest_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    

class Loan(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('credit', 'Credit'),
        ('debit', 'Debit')
    ]
    
    account_number = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_id = models.AutoField(primary_key=True)
    principal = models.DecimalField(max_digits=10, decimal_places=2)
    next_payment_due = models.DateField()
    interest_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateField()
    loan_term = models.IntegerField()
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES, default='debit')


class Saving(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('credit', 'Credit'),
        ('debit', 'Debit')
    ]
    
    account_number = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_id = models.AutoField(primary_key=True)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateField()
    transaction_desc = models.CharField(max_length=100)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES, default='credit')


class Check(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('credit', 'Credit'),
        ('debit', 'Debit')
    ]
    
    account_number = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_id = models.AutoField(primary_key=True)
    principal = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateField()
    transaction_desc = models.CharField(max_length=100)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES, default='debit')


class CreditCard(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('credit', 'Credit'),
        ('debit', 'Debit')
    ]
    
    account_number = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_id = models.AutoField(primary_key=True)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateField()
    transaction_desc = models.CharField(max_length=100)
    last_payment_date = models.DateField()
    next_payment_date = models.DateField()
    credit_limit = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_payment = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES, default='debit')

    