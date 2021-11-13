from django.shortcuts import render,redirect
from django.views import View
from .models import *
from .forms import *
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from random import randint
# Create your views here.

#def product_detail(request):
 #return render(request, 'app/productdetail.html')
class ProductView(View):
    def get(self,request):
        topwear=Product.objects.filter(category='TW')
        bottomwear=Product.objects.filter(category='BW')
        mobile=Product.objects.filter(category='M')
        laptop=Product.objects.filter(category='L')
        context={
            'topwears':topwear,
            'bottomwears':bottomwear,
            'laptops':laptop,
            'mobiles':mobile
        }
        return render(request,'app/home.html',context)


class ProductDetailView(View):
    def get(self,request,pk):
        user=request.user
        product=Product.objects.get(id=pk)
        item_already_in_cart=False
        item_already_in_wishlist=False
       # item_already_in_cart=Cart.objects.filter(Q(product=product)  &  Q(user=request.user)).exists()
        if user.is_authenticated:
            item_already_in_cart=Cart.objects.filter(Q(product=product.id)  &  Q(user=request.user)).exists()
        #item_already_in_cart=Cart.objects.filter(Q(product.id=product.id)  &  Q(user=request.user)).exists()
       # item_already_in_cart=Cart.objects.filter(Q(product.id=product)  &  Q(user=request.user)).exists()
       #have to find the differences between all these
        if user.is_authenticated:
           item_already_in_wishlist=Wishlist.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
           
        context={
            'product':product,
            'item_exists':item_already_in_cart,
            'item_in_wishlist':item_already_in_wishlist
            }
        
        return render(request,'app/productdetail.html',context)

def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    if Cart.objects.filter(Q(product=product)  &  Q(user=user)).exists():
       pass
    else:
        Cart(user=user,product=product,quantity=1).save()
    return redirect('product-detail',product_id)


def show_cart(request):
    if request.user.is_authenticated:
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0.0
        shipping=70.0
        total=0.0
        cart_product=[p for p in Cart.objects.all() if p.user == user]
        #for x in cart:
          #  total+=x.product.discounted_price
        if cart_product:
            for p in cart_product:
                tempamount=(p.quantity * p.product.discounted_price)
                amount+=tempamount
                total=amount+shipping    
            return render(request, 'app/cart.html',{'carts':cart,'total':total,'shipping':shipping,'amount':amount})  
        else:
            return render(request,'app/emptycart.html')

def pluscart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        print(prod_id)
        c=Cart.objects.get(Q(product=prod_id)  &  Q(user=request.user))
        c.quantity+=1
        c.save()
        amount=0.0
        shipping=70.0
        cart_product=[p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount=(p.quantity * p.product.discounted_price)
            amount+=tempamount
          
        data={
            'quantity':c.quantity,
             'amount':amount,
            'totalamount':amount+shipping 
            }           
        return JsonResponse(data)

def minuscart(request):
    if request.method == 'GET':
        prod_id=request.GET.get('prod_id')
        c=Cart.objects.get(Q(product=prod_id)  &  Q(user=request.user))
        if c.quantity ==0:
           pass
        c.quantity-=1
        c.save()
        amount=0.0
        shipping=70.0
        cart_product=[p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount=(p.quantity * p.product.discounted_price)
            amount+=tempamount
             
        data={
            'quantity':c.quantity,
             'amount':amount,
            'totalamount':amount+shipping
            }           
        return JsonResponse(data)
        #return redirect('/cart')

def removecart(request,pk):
    print('def')
    if request.method == 'GET':
        #prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=pk)  &  Q(user=request.user))
        c.delete()
        amount=0.0
        shipping=70.0
        cart_product=[p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount=(p.quantity * p.product.discounted_price)
            amount+=tempamount 
        data={
             'amount':amount,
            'totalamount':amount+shipping 
            }           
        #return JsonResponse(data)
        return redirect('/cart')

    
            

def buyNow(request,pk):
    print('buy')
    user=request.user
    product=Product.objects.get(id=pk)
    if Cart.objects.filter(Q(product=pk)  &  Q(user=user)).exists():
       pass
    else:
        Cart(user=user,product=product,quantity=1).save()
    cart=Cart.objects.filter(Q(product=pk)  &  Q(user=user))
    add=Customer.objects.filter(user=user)
    return render(request,'app/checkout.html',{'cart':cart,'add':add})


def address(request):
    addresses=Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':addresses,'active':'btn-primary'})

@login_required
def orders(request):
    orders=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'orders':orders})

def change_password(request):
 return render(request, 'app/changepassword.html')

def MobileView(request,data=None,num=None):
    print('def')
    mobiles=Product.objects.filter(category='M')
    mobile_brand=set()
    for name in mobiles:
        mobile_brand.add(name.brand) 
    
    if data == None and num==None:
        print('if')
        mobiles=Product.objects.filter(category='M')
    elif data == data and num==None:
        print('elif1')
        mobiles=Product.objects.filter(category='M').filter(brand=data)
    elif data == None and num==num:
        if num == 10000:
            mobiles=Product.objects.filter(category='M').filter(discounted_price__lt=10000)
        elif num == 20000:
             mobiles=Product.objects.filter(category='M').filter(discounted_price__gt=10000)
    
    return render(request, 'app/mobile.html',{'mobiles':mobiles,'mobilebrands':mobile_brand})


def login(request):
 return render(request, 'app/login.html')

#def customerregistration(request):
 #return render(request, 'app/customerregistration.html')

class CustomerRegistrationView(View):
    def get(self,request):
        form=customerRegistrationForm()
        return render(request, 'app/customerregistration.html',{'form':form})

    def post(self,request):
        form=customerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'success')
        return render(request, 'app/customerregistration.html',{'form':form})
        

def checkout(request):
    user=request.user
    add=Customer.objects.filter(user=user)
    cart_items=Cart.objects.filter(user=user)
    amount=0.0
    shipping=70
    total=0.0
    cart_product=[p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount=(p.quantity * p.product.discounted_price)       
            amount+=tempamount
        total=amount+shipping         
    return render(request, 'app/checkout.html',{'add':add,'cart':cart_items,'total':total})

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm()
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})

    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            reg=Customer(user=user,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,'congrats profile successfully updated')
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
#form.cleaned_data or form.is_valid() any method can be used

def paymentdone(request):
    user=request.user
    custid=request.GET['custid']    #request.GET.get('custid')>>>both are valid
    customer=Customer.objects.get(id=custid)
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect('orders')

def laptopView(request,data=None):
    laptops=Product.objects.filter(category='L')
    laptop_brand=set()
    for name in laptops:
        laptop_brand.add(name.brand) 

    if data == None:
        laptops=Product.objects.filter(category='L')

    elif data == data:
        laptops=Product.objects.filter(category='L').filter(brand=data)

    return render(request,'app/laptops.html',{'laptops':laptops,'laptopbrands':laptop_brand})

def topwearView(request,data=None):
    topwears=Product.objects.filter(category='TW')
    topwear_brand=set()
    for name in topwears:
        topwear_brand.add(name.brand) 

    if data == None:
        topwears=Product.objects.filter(category='TW')

    elif data == data:
        topwears=Product.objects.filter(category='TW').filter(brand=data)
    print(topwear_brand)

    return render(request,'app/topwear.html',{'topwears':topwears,'topwearbrands':topwear_brand})

def bottomwearView(request,data=None):
    bottomwears=Product.objects.filter(category='BW')
    bottomwear_brand=set()
    for name in bottomwears:
        bottomwear_brand.add(name.brand) 

    if data == None:
        bottomwears=Product.objects.filter(category='BW')

    elif data == data:
        bottomwears=Product.objects.filter(category='BW').filter(brand=data)

    return render(request,'app/bottomwear.html',{'bottomwears':bottomwears,'bottomwearbrands':bottomwear_brand})

def search(request):
    product_objects=Product.objects.all()
    name=request.GET.get('search')
    print('def')
    if name !='' and name is not None:
        print('if')
        product_objects=product_objects.filter(title__icontains=name)
    return render(request,'app/searchresult.html',{'products':product_objects})

def wishlistView(request):
    products=Wishlist.objects.filter(user=request.user)
    return render(request,'app/wishlist.html',{'products':products})
  

def addToWishlistView(request,pk):
    user=request.user
    product=Product.objects.get(id=pk)
    Wishlist(user=user,product=product).save()  
    return redirect('product-detail',pk)

def removeWishlistView(request,pk):
    if request.user.is_authenticated:
        product=Product.objects.get(id=pk)
        wishlist_product=Wishlist.objects.get(Q(user=request.user) & Q(product=product))
        wishlist_product.delete()
    return redirect('product-detail',pk)


    








    
