# Generated by Django 4.2.3 on 2023-07-17 18:13

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bankingApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='account_type',
            field=models.CharField(choices=[('checking', 'Checking'), ('savings', 'Savings'), ('credit_card', 'Credit Card'), ('loan', 'Loan')], default='checking', max_length=20),
        ),
        migrations.AlterField(
            model_name='account',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='account',
            name='customer_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='bankingApp.customer'),
        ),
        migrations.AlterField(
            model_name='account',
            name='date_opened',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='account',
            name='interest_rate',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='account',
            name='overdraft_lim',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]