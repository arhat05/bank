from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Customer)
admin.site.register(Account)
admin.site.register(Loan)
admin.site.register(Saving)
admin.site.register(Check)
admin.site.register(CreditCard)
