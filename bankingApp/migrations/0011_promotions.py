# Generated by Django 4.2.3 on 2023-08-10 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bankingApp', '0010_alter_creditcard_last_payment_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promotions',
            fields=[
                ('promotion_id', models.AutoField(primary_key=True, serialize=False)),
                ('promotion_name', models.CharField(max_length=50)),
                ('promotion_desc', models.CharField(max_length=100)),
                ('promotion_details', models.CharField(max_length=100)),
            ],
        ),
    ]
