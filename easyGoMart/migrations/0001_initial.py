# Generated by Django 4.1.7 on 2023-11-05 12:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('phoneNo', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('customerName', models.CharField(max_length=100)),
                ('customerEmail', models.TextField()),
                ('password', models.TextField()),
                ('deliveryAddress', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('orderID', models.IntegerField(primary_key=True, serialize=False)),
                ('deliveryMethod', models.TextField(default='null')),
                ('paymentMethod', models.TextField(default='null')),
                ('totalAmount', models.FloatField(default=0)),
                ('orderDate', models.DateTimeField()),
                ('orderStatus', models.CharField(max_length=9)),
                ('phoneNo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='easyGoMart.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('productID', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('productImg', models.ImageField(upload_to='')),
                ('productName', models.TextField()),
                ('productDesc', models.TextField()),
                ('productCategory', models.CharField(max_length=30)),
                ('productPrice', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('staffID', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('staffName', models.CharField(max_length=100)),
                ('password', models.TextField(default='null')),
            ],
        ),
        migrations.CreateModel(
            name='TransactionDetail',
            fields=[
                ('transactionID', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('transactionImg', models.ImageField(default='', upload_to='')),
                ('transactionBankName', models.TextField(default='null')),
                ('transactionMethod', models.TextField(default='null')),
                ('transactionDate', models.DateTimeField(default='')),
                ('transactionStatus', models.CharField(default='', max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('cartID', models.IntegerField(primary_key=True, serialize=False)),
                ('productQuantity', models.IntegerField(default=0)),
                ('phoneNo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='easyGoMart.customer')),
                ('productID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='easyGoMart.product')),
            ],
        ),
        migrations.CreateModel(
            name='OrderList',
            fields=[
                ('cartID', models.IntegerField(primary_key=True, serialize=False)),
                ('productQuantity', models.IntegerField(default=0)),
                ('orderID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='easyGoMart.orderdetail')),
                ('phoneNo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='easyGoMart.customer')),
                ('productID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='easyGoMart.product')),
            ],
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='transactionID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='easyGoMart.transactiondetail'),
        ),
    ]
