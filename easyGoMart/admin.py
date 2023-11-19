from django.contrib import admin
from .models import Staff,Customer,Product,ShoppingCart,OrderDetail,TransactionDetail,OrderList
# Register your models here.
admin.site.register(Staff)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(ShoppingCart)
admin.site.register(OrderDetail)
admin.site.register(TransactionDetail)
admin.site.register(OrderList)

