from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse,HttpResponseBadRequest  ,JsonResponse
from django.urls import reverse
from .models import Staff, Customer,Product,ShoppingCart, OrderDetail, TransactionDetail,OrderList
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils import timezone
from datetime import datetime

# Create your views here.
# homepage 
def homePage(request):
    return render (request,"homePage.html")

def selectLogin(request):
    return render (request,"selectLogin.html")

# customer authentication functions
def signUpCustomer(request, success_msg=None):
    if request.method == 'POST':
        phoneNo = request.POST.get('phoneNo')
        customerName = request.POST.get('customerName')
        customerEmail = request.POST.get('customerEmail')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')
        deliveryAddress = request.POST.get('deliveryAddress')
        
        # Check if customer exists in the database
        if Customer.objects.filter(phoneNo=phoneNo).exists():
            error_msg = "The phone number already exists. Please choose a different number."
            return render(request, 'signUpCustomer.html', {'error_msg': error_msg})

        # If password field is empty
        if not password:
            error_msg = "No password input detected. Please enter an appropriate password."
            return render(request, 'signUpCustomer.html', {'error_msg': error_msg})

        # If password is not appropriate
        if len(password) < 8:
            error_msg = "Please enter an appropriate password."
            return render(request, 'signUpCustomer.html', {'error_msg': error_msg})
        
        # If confirm password not correct
        if confirmPassword != password:
            error_msg = "Password and confirm password do not match."
            return render(request, 'signUpCustomer.html', {'error_msg': error_msg})

        # Create new customer
        customer = Customer(phoneNo=phoneNo, customerName=customerName, customerEmail=customerEmail, password=password, deliveryAddress=deliveryAddress)
        customer.save()
        success_msg = "Sign up is successful."
        return redirect(reverse('signUpSuccess', args=[success_msg]))
        
    return render(request, 'signUpCustomer.html', {'success_msg': success_msg})

def loginCustomer(request):
    if request.method == 'POST':
        phoneNo = request.POST.get('phoneNo')
        password = request.POST.get('password')
        if not phoneNo or not password:
            return render(request, 'loginCustomer.html', {'error_message': 'Missing required fields. Please input the data correctly.'})
        try:
            customer = Customer.objects.get(phoneNo=phoneNo)
        except Customer.DoesNotExist:
            return render(request, 'loginCustomer.html', {'error_message': 'Incorrect phone number or password. Please input the correct data into each field.'})
        if customer.password != password:
            return render(request, 'loginCustomer.html', {'error_message': 'Incorrect password. Please input the correct data into each field.'})
        else:
            request.session['phoneNo'] = phoneNo
            return HttpResponseRedirect(reverse('productsPage'))  
    else:
        return render(request, 'loginCustomer.html')

# logout session function
def logout(request):
    del request.session['phoneNo']
    messages.success(request, 'You have logged out successfully')
    return redirect('loginCustomer')

def logoutStaff(request):
    del request.session['staffID']
    messages.success(request, 'You have logged out successfully')
    return redirect('loginStaff')

# customer page functions
def productsPage(request):
    # to display customer info after login
    if 'phoneNo' not in request.session:
        return HttpResponseRedirect(reverse('loginCustomer'))
    else:
        phoneNo = request.session['phoneNo']
        customer = Customer.objects.get(phoneNo=phoneNo)
        customerData = Customer.objects.all()
        products = Product.objects.all()
        dataDict= {
           'customerName': customer.customerName,
           'customerData': customerData,
           'products': products,
        }
    return render(request, "productsPage.html", dataDict)

# search and filter products
def productsPageFilter(request):
    if 'phoneNo' not in request.session:
        return HttpResponseRedirect(reverse('loginCustomer'))
    else:
        phoneNo = request.session['phoneNo']
        customer = Customer.objects.get(phoneNo=phoneNo)
        customerData = Customer.objects.all()

        search_query = request.GET.get('search', '')
        category = request.GET.get('category', '')

        products = Product.objects.filter(productName__icontains=search_query)
        if category != 'All':
            products = products.filter(productCategory=category)

        dataDict= {
           'customerName': customer.customerName,
           'customerData': customerData,
           'products': products,
           'search_query': search_query,
           'category': category,
        }

    return render(request, "productsPageFilter.html", dataDict)

def manageCustomerAccount(request):
    # to display customer info after login
    if 'phoneNo' not in request.session:
        return HttpResponseRedirect(reverse('loginCustomer'))
    else:
        phoneNo = request.session['phoneNo']
        customer = Customer.objects.get(phoneNo=phoneNo)
        custData ={
           'customerName': customer.customerName,
        }
    return render (request,'customerAccountPage.html',custData)

# update customer profile information
def customerUpdateProfile(request):
    if 'phoneNo' not in request.session:
        return HttpResponseRedirect(reverse('loginCustomer'))
    else:
        phoneNo = request.session['phoneNo']
        customer = Customer.objects.get(phoneNo=phoneNo)
        
        if request.method == 'POST':
            customerName = request.POST.get('name')
            customerEmail = request.POST.get('email')
            deliveryAddress = request.POST.get('deliveryAddress')
            
            # Update the customer's profile
            customer.customerName = customerName
            customer.customerEmail = customerEmail
            customer.deliveryAddress = deliveryAddress
            customer.save()

            messages.success(request, 'Profile updated successfully.')
            return redirect('customerUpdateProfile')  

        custData ={
           'customer': customer,  
        }
    return render(request, 'customerUpdateProfile.html', custData)

#update customer password
def customerUpdatePassword(request):
    if 'phoneNo' not in request.session:
        return HttpResponseRedirect(reverse('loginCustomer'))
    else:
        phoneNo = request.session['phoneNo']
        customer = Customer.objects.get(phoneNo=phoneNo)
        
        if request.method == 'POST':
            currentPassword = request.POST.get('password')
            newPassword = request.POST.get('newPassword')
            confirmPassword = request.POST.get('confirmPassword')
            
            # Check if current password is correct
            if currentPassword != customer.password:
                messages.error(request, 'Current password is incorrect.')
                return redirect('customerUpdatePassword')
            
            # Check if new password same as the confirmed password
            if newPassword != confirmPassword:
                messages.error(request, 'New password and confirm password do not match.')
                return redirect('customerUpdatePassword')
            
            else:
                customer.password = newPassword
                customer.save()
                messages.success(request, 'Password updated successfully.')
                return redirect('customerUpdatePassword') 

        custData ={
           'customer': customer,
        }

    return render(request, 'customerUpdatePassword.html', custData)

#add item to cart
def addToCart(request, product_id):
    if 'phoneNo' not in request.session:
        return HttpResponseRedirect(reverse('loginCustomer'))
    else:
        phoneNo = request.session['phoneNo']
        customer = Customer.objects.get(phoneNo=phoneNo)
        product = get_object_or_404(Product, productID=product_id)
        
        # Create or update the shopping cart entry
        cart, created = ShoppingCart.objects.get_or_create(
            phoneNo=customer,
            productID=product,
            defaults={'productQuantity': 1}  # Default quantity is 1
        )
        
        # increment the quantity of item
        if not created:
            cart.productQuantity += 1
            cart.save()

        messages.success(request, 'Item added to cart successfully.')
        return HttpResponseRedirect(reverse('productsPage'))

#calculate total fees based on receive method
def calculateTotalFees(receiveMethod, shopping_cart):
    totalFees = 0
    if receiveMethod == 'delivery':
        totalFees = 3 + len(shopping_cart)  
    return totalFees

#save new transaction, order
def generateTransactionId():
    latestTransaction = TransactionDetail.objects.order_by('-transactionID').first()
    if latestTransaction is not None:
        latestId = int(latestTransaction.transactionID[2:])
        newId = f'TX{latestId + 1:03}'
    else:
        newId = 'TX001'
    return newId

def generateOrderID():
    latestOrder = OrderDetail.objects.order_by('-orderID').first()
    if latestOrder is not None:
        latestId = int(latestOrder.orderID)
        newId = f'{latestId + 1:03}'
    else:
        newId = '001'
    return newId

#delete from cart
def deleteCartItem(request, cart_id):
    if 'phoneNo' not in request.session:
        return HttpResponseRedirect(reverse('logincustomer'))
    else:
        try:
            cart_item = ShoppingCart.objects.get(cartID=cart_id)
            cart_item.delete()
        except ShoppingCart.DoesNotExist:
            pass  # Handle the case where the item does not exist

        return HttpResponseRedirect(reverse('shoppingCart'))

# shoppingCart 
def shoppingCart(request):
    if 'phoneNo' not in request.session:
        return HttpResponseRedirect(reverse('logincustomer'))
    else:
        phoneNo = request.session['phoneNo']
        customer = Customer.objects.get(phoneNo=phoneNo)
    
        shoppingCart = ShoppingCart.objects.filter(phoneNo=customer)
        totalFees = 0
        totalAmount = 0
        totalPrice = 0  
        
        shoppingCartData = {  
            'customer': customer,
            'shoppingCart': shoppingCart,
            'totalFees': totalFees,  
            'totalAmount': totalAmount,
        }

        if request.method == 'POST':
            for item in shoppingCart:
                quantity = request.POST.get(f'quantity_{item.cartID}')
                item.productQuantity = quantity
                item.save()
                totalPrice = item.productID.productPrice * int(quantity)
                item.totalPrice = totalPrice
                item.save()

            receiveMethod = request.POST.get('receiveMethod')
            totalFees = calculateTotalFees(receiveMethod, shoppingCart)
            totalAmount = sum(item.totalPrice for item in shoppingCart) + totalFees

            shoppingCartData['totalFees'] = totalFees  
            shoppingCartData['totalAmount'] = totalAmount  
            shoppingCartData['shoppingCart'].paymentMethod = request.POST.get('paymentMethod')
            shoppingCartData['shoppingCart'].deliveryMethod = request.POST.get('receiveMethod')    

        # Save to transaction, order details and orderlist
        if 'submitOrder' in request.POST:
            transactionId = generateTransactionId()
            transaction = TransactionDetail(
                transactionID=transactionId,
                transactionImg=None,  
                transactionBankName="EasyGo or Bank Name",  
                transactionMethod="fill method here",  
                transactionDate=timezone.now(),
                transactionStatus="pending approval"  
            )
            transaction.save()

            orderId = generateOrderID()
            order = OrderDetail(
                orderID=orderId,
                transactionID=transaction,
                phoneNo=customer,
                deliveryMethod=request.POST.get('receiveMethod'),
                paymentMethod=request.POST.get('paymentMethod'),
                totalAmount=totalAmount,
                orderDate=timezone.now(),
                orderStatus='preparing',
            )
            order.save()

            for item in shoppingCart:
                orderlist = OrderList(
                    phoneNo=customer,
                    orderID=order,
                    productID=item.productID,
                    productQuantity=item.productQuantity
                )
                orderlist.save()

            shoppingCartData['orderSuccess'] = True
            return redirect('updatePaymentDetails', transaction_id=transactionId)

        return render(request, 'shoppingCart.html', shoppingCartData)

# payment details page
def paymentDetails(request):
    if 'phoneNo' not in request.session:
        return HttpResponseRedirect(reverse('logincustomer'))
    else:
        phoneNo = request.session['phoneNo']
        customer = Customer.objects.get(phoneNo=phoneNo)
        transaction_details = TransactionDetail.objects.filter(phoneNo=customer)

        data = {
            'phoneNo': phoneNo,
            'customer': customer,
            'transaction_details': transaction_details,  
        }
        return render(request, 'paymentDetails.html', data)

#update payment
def updatePaymentDetails(request, transaction_id):
    if 'phoneNo' not in request.session:
        return HttpResponseRedirect(reverse('logincustomer'))
    else:
        phoneNo = request.session['phoneNo']
        customer = Customer.objects.get(phoneNo=phoneNo)
        transaction = get_object_or_404(TransactionDetail, transactionID=transaction_id)
        
        if request.method == 'POST':
            transaction.transactionImg = request.FILES.get('transactionImg', transaction.transactionImg)
            transaction.transactionBankName = request.POST.get('transactionBankName', transaction.transactionBankName)
            transaction.transactionMethod = request.POST.get('transactionMethod', transaction.transactionMethod)
            transaction.transactionDate=timezone.now()
            transaction.save()

            return redirect('successPayment')  

        data = {
            'phoneNo': phoneNo,
            'customer': customer,
            'transaction': transaction,
        }
        return render(request, 'updatePaymentDetails.html', data)

# successPayment
def successPayment(request):
        if 'phoneNo' not in request.session:
            return HttpResponseRedirect(reverse('logincustomer'))
        else:
            phoneNo = request.session['phoneNo']
            customer = Customer.objects.get(phoneNo=phoneNo)

        data={
            'phoneNo' : phoneNo,
            'customer': customer,

        }
        return render(request, 'successPayment.html', data)

#customer Order list
def customerOrderList(request):
    if 'phoneNo' not in request.session:
        return HttpResponseRedirect(reverse('logincustomer'))
    else:
        phoneNo = request.session['phoneNo']
        customer = Customer.objects.get(phoneNo=phoneNo)
        order_details = OrderDetail.objects.filter(phoneNo=customer)
        success_message = request.GET.get('success_message')  

    data = {
        'phoneNo': phoneNo,
        'customer': customer,
        'order_details': order_details,
        'success_message': success_message
    }
    return render(request, 'customerOrderList.html', data)

def updateOrderStatus(request):
    if request.method == 'GET' and 'orderID' in request.GET:
        orderID = request.GET['orderID']
        try:
            order_detail = OrderDetail.objects.get(orderID=orderID)
            order_detail.orderStatus = 'received'
            order_detail.save()
            success_message = 'Order status updated successfully'
        except OrderDetail.DoesNotExist:
            success_message = 'Order does not exist'

    return HttpResponseRedirect(reverse('customerOrderList') + f'?success_message={success_message}')

#====================================================================================================================================================================
# staff authentication
def loginStaff(request):
    if request.method == 'POST':
        staffID = request.POST.get('staffID')
        password = request.POST.get('password')
        if not staffID or not password:
            return render(request, 'loginStaff.html', {'error_message': 'Missing required fields. Please input the data correctly.'})
        try:
            staff = Staff.objects.get(staffID=staffID)
        except Staff.DoesNotExist:
            return render(request, 'loginStaff.html', {'error_message': 'Incorrect staff ID or password. Please input the correct data into each field.'})
        if staff.password != password:
            return render(request, 'loginStaff.html', {'error_message': 'Incorrect password. Please input the correct data into each field.'})
        else:
            request.session['staffID'] = staffID
            return HttpResponseRedirect(reverse('staffPage'))
    else:
        return render(request, 'loginStaff.html')

# staff functions
def staffPage(request):
    if 'staffID' not in request.session:
        return HttpResponseRedirect(reverse('loginStaff'))
    else:
        staffID = request.session['staffID']
        staff = Staff.objects.get(staffID=staffID)
        products = Product.objects.all()
        dataDict= {
           'staffName': staff.staffName,
           'products': products,
        }
    
    return render (request,"staffPage.html",dataDict)

def staffPageFilter(request):
    if 'staffID' not in request.session:
        return HttpResponseRedirect(reverse('loginStaff'))
    else:
        staffID = request.session['staffID']
        staff = Staff.objects.get(staffID=staffID)

        search_query = request.GET.get('search', '')
        category = request.GET.get('category', 'All')

        products = Product.objects.all()
        if search_query:
            products = products.filter(productName__icontains=search_query)
        if category != 'All':
            products = products.filter(productCategory=category)

        dataDict = {
            'staffName': staff.staffName,
            'products': products,
            'search_query': search_query,
            'category': category,
        }

    return render(request, "staffPageFilter.html", dataDict)

#staff update products
def updateProduct(request, product_id):
    if 'staffID' not in request.session:
        return HttpResponseRedirect(reverse('loginStaff'))
    else:
        staffID = request.session['staffID']
        staff = Staff.objects.get(staffID=staffID)
        product = get_object_or_404(Product, productID=product_id)

        if request.method == 'POST':
            product.productName = request.POST['productName']
            product.productDesc = request.POST['productDesc']
            product.productCategory = request.POST['productCategory']
            product.productPrice = request.POST['productPrice']
        
            if request.FILES.get('productImg'):
                productImg = request.FILES['productImg']
                filename = default_storage.save(productImg.name, ContentFile(productImg.read()))
                product.productImg = filename

            product.save()
            messages.success(request, 'Product updated successfully.')

        dataDict = {
            'staffName': staff.staffName,
            'product': product,
        }
        return render (request,"staffUpdateProduct.html",dataDict)

#order list details
def staffOrderDetails(request):
    if 'staffID' not in request.session:
        return HttpResponseRedirect(reverse('loginStaff'))
    else:
        staffID = request.session['staffID']
        staff = Staff.objects.get(staffID=staffID)
        
        order_details = OrderDetail.objects.all()

        # Calculation
        total_sales = sum(order_detail.totalAmount for order_detail in order_details)

    data = {
        'staffID': staffID,
        'staff': staff,
        'staffName': staff.staffName,
        'order_details': order_details, 
        'total_sales': total_sales  
    }
    return render(request, 'staffOrderDetails.html', data)

# view customer order details
def viewOrderDetails(request, order_id):
    if 'staffID' not in request.session:
        return HttpResponseRedirect(reverse('loginStaff'))
    else:
        staffID = request.session['staffID']
        staff = Staff.objects.get(staffID=staffID)

        order_detail = get_object_or_404(OrderDetail, orderID=order_id)

        data = {
            'staffID': staffID,
            'staff': staff,
            'staffName': staff.staffName,
            'order_detail': order_detail, 
        }

        return render(request, 'viewCustomerOrder.html', data)

# staff update customer order status 
def staffUpdateOrderStatus(request, order_id):
    if request.method == 'POST':
        order_status = request.POST.get('orderStatus')
        order_detail = OrderDetail.objects.get(orderID=order_id)
        order_detail.orderStatus = order_status
        order_detail.save()
    
    messages.success(request, 'Order status successfully updated!')
    return HttpResponseRedirect(reverse('viewOrderDetails', args=[order_id]))

#staff view payment details
def staffViewPayment(request, order_id):
    if 'staffID' not in request.session:
        return HttpResponseRedirect(reverse('loginStaff'))
    else:
        staffID = request.session['staffID']
        staff = Staff.objects.get(staffID=staffID)

        order_detail = get_object_or_404(OrderDetail, orderID=order_id)
        transaction_detail = order_detail.transactionID  

        data = {
            'staffID': staffID,
            'staff': staff,
            'staffName': staff.staffName,
            'order_detail': order_detail,
            'transaction_detail': transaction_detail, 
        }
        return render(request, 'staffViewPayment.html', data)

#update payment status
def updateTransactionStatus(request):
    if request.method == 'POST':
        order_id = request.POST.get('orderID')
        transaction_status = request.POST.get('transactionStatus')
        
        try:
            order_detail = OrderDetail.objects.get(orderID=order_id)
            order_detail.transactionID.transactionStatus = transaction_status
            order_detail.transactionID.save()
            
            messages.success(request, 'Transaction status updated successfully!')
        except OrderDetail.DoesNotExist:
            messages.error(request, 'Order does not exist')
        
        return redirect('staffViewPayment', order_id=order_id)
    
# sales report
def salesReport(request):
    if 'staffID' not in request.session:
        return HttpResponseRedirect(reverse('loginStaff'))
    else:
        staffID = request.session['staffID']
        staff = Staff.objects.get(staffID=staffID)

        completed_orders = OrderDetail.objects.filter(orderStatus='complete')

        items_dict = {}  
        total_sales = 0

        for order in completed_orders:
            order_list = OrderList.objects.filter(orderID=order)
            for item in order_list:
                item_name = item.productID.productName
                quantity_sold = item.productQuantity

                if item_name in items_dict:
                    items_dict[item_name] += quantity_sold
                else:
                    items_dict[item_name] = quantity_sold

        total_sales = sum(order.totalAmount for order in completed_orders)
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
        items = [{'itemName': name, 'quantitySold': quantity} for name, quantity in items_dict.items()]

        data = {
            'staffID': staffID,
            'staff': staff,
            'staffName': staff.staffName,
            'items': items,
            'totalSales': total_sales,
            'currentDate': current_date,
        }

        return render(request, 'salesReport.html', data)
