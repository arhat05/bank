# Generated by Django 4.2.3 on 2023-07-27 04:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bankingApp', '0006_alter_check_principal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='creditcard',
            name='principal',
        ),
        migrations.RemoveField(
            model_name='saving',
            name='principal',
        ),
    ]