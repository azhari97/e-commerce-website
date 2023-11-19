from django.urls import path
from . import views

urlpatterns = [
    path("", views.homePage, name="homePage"),

    # sign in and sign up urls
    path('selectLogin/', views.selectLogin, name='selectLogin'),

    #customer authentication 
    path('loginCustomer/', views.loginCustomer, name='loginCustomer'),   
    path('signUpCustomer/', views.signUpCustomer, name='signUpCustomer'),
    path('signUpCustomer/<str:success_msg>/', views.signUpCustomer, name='signUpSuccess'),
    
    #customer pages and etc
    path("productsPage/", views.productsPage, name="productsPage"),
    path('productsPageFilter/', views.productsPageFilter, name='productsPageFilter'),
    path('logout/', views.logout, name='logout'),
    path("manageCustomerAccount/", views.manageCustomerAccount, name="manageCustomerAccount"),
    # manage customer data and password
    path("customerUpdateProfile/", views.customerUpdateProfile, name="customerUpdateProfile"),
    path('customer/account/', views.customerUpdateProfile, name='customerUpdateProfile'),
    path("customerUpdatePassword/", views.customerUpdatePassword, name="customerUpdatePassword"),
    path('customer/updatedPassword/', views.customerUpdatePassword, name='customerUpdatePassword'),
    # customer add/remove item to cart
    path('add_to_cart/<str:product_id>/', views.addToCart, name='addToCart'),
    path('deleteCartItem/<int:cart_id>/', views.deleteCartItem, name='deleteCartItem'),
    # customer shop cart
    path('shoppingCart/', views.shoppingCart, name='shoppingCart'),
    #path('paymentDetails/', views.paymentDetails, name='paymentDetails'),
    path('updatePaymentDetails/<str:transaction_id>/', views.updatePaymentDetails, name='updatePaymentDetails'),
    path('successPayment/', views.successPayment, name='successPayment'),
    path('customerOrderList/', views.customerOrderList, name='customerOrderList'),
    path('updateOrderStatus/', views.updateOrderStatus, name='updateOrderStatus'),

    #staff authentication 
    path('loginStaff/', views.loginStaff, name='loginStaff'),
    path('logoutStaff/', views.logoutStaff, name='logoutStaff'),

    #staff pages and etc
    path("staffPage/", views.staffPage, name="staffPage"),
    path('staffPageFilter/', views.staffPageFilter, name='staffPageFilter'),
    path('updateProduct/<str:product_id>/', views.updateProduct, name='updateProduct'),
    path('staffOrderDetails/', views.staffOrderDetails, name='staffOrderDetails'),
    # list customer order n payment pages 
    path('viewOrderDetails/<int:order_id>/', views.viewOrderDetails, name='viewOrderDetails'),
    #update order status path
    path('staffUpdateOrderStatus/<int:order_id>/', views.staffUpdateOrderStatus, name='staffUpdateOrderStatus'),
    path('staffViewPayment/<int:order_id>/', views.staffViewPayment, name='staffViewPayment'),
    path('updateTransactionStatus/', views.updateTransactionStatus, name='updateTransactionStatus'),

    path('salesReport/', views.salesReport, name='salesReport'),

]
