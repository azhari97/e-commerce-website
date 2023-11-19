
# Create your models here.
from django.db import models

# Create your models here.
class Staff(models.Model):
    staffID = models.CharField(max_length= 5, primary_key= True)
    staffName = models.CharField(max_length=100)
    password = models.TextField(default='null')

class Customer(models.Model):
    phoneNo = models.CharField(max_length= 12, primary_key= True)
    customerName = models.CharField(max_length=100)
    customerEmail = models.TextField()
    password = models.TextField()
    deliveryAddress = models.CharField(max_length=300)

class Product(models.Model):
    productID = models.CharField(max_length= 5, primary_key= True)
    productImg = models.ImageField()
    productName = models.TextField()
    productDesc = models.TextField()
    productCategory = models.CharField(max_length=30)
    productPrice = models.FloatField()

class TransactionDetail(models.Model):
    transactionID = models.CharField(max_length= 5, primary_key= True)
    transactionImg = models.ImageField(default='')
    transactionBankName = models.TextField(default="null")
    transactionMethod = models.TextField(default="null")
    transactionDate = models.DateTimeField(default='')
    transactionStatus = models.CharField(max_length=16,default='') #not approved-12 or approved or pending approval

class ShoppingCart(models.Model):
    cartID = models.IntegerField(primary_key= True)
    phoneNo = models.ForeignKey(Customer, on_delete=models.CASCADE)
    productID = models.ForeignKey(Product, on_delete=models.CASCADE)
    productQuantity = models.IntegerField(default=0)

class OrderDetail(models.Model):
    orderID = models.IntegerField(primary_key=True)
    transactionID = models.ForeignKey(TransactionDetail, on_delete=models.CASCADE)
    phoneNo = models.ForeignKey(Customer, on_delete=models.CASCADE)
    deliveryMethod = models.TextField(default="null")
    paymentMethod = models.TextField(default="null")
    totalAmount = models.FloatField(default=0)
    orderDate = models.DateTimeField()
    orderStatus = models.CharField(max_length=9) #cancelled, preparing-9, shipped, received, complete

class OrderList(models.Model):
    itemNo = models.IntegerField(primary_key= True)
    phoneNo = models.ForeignKey(Customer, on_delete=models.CASCADE)
    orderID = models.ForeignKey(OrderDetail, on_delete=models.CASCADE)
    productID = models.ForeignKey(Product, on_delete=models.CASCADE)
    productQuantity = models.IntegerField(default=0)
    

