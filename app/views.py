from django.shortcuts import render , redirect , HttpResponse
from django.views import View
from .models import Customer , Product , Cart , OrderPLaced 
from .forms import CustomerRegistrationForm , CustomerProfileForm
from django.contrib import messages
from django.db.models import Q 
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
class ProductView(View):
 def get(self , request):
  topwears = Product.objects.filter(category="TW")
  bottomwears = Product.objects.filter(category='BW')
  mobiles=Product.objects.filter(category="M")
  return render(request , 'app/home.html', {'topwears':topwears , 'bottomwears':bottomwears,'mobiles':mobiles})


class ProductDetailView(View):  
 def get(self , request , pk):
  product = Product.objects.get(pk=pk)
  item_already_in_cart = False
  if request.user.is_authenticated:
    item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()

  return render(request, 'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart})
  
def login(request):
 return render(request,"app/login.html")

@login_required
def add_to_cart(request):
 user = request.user
 product_id = request.GET.get('prod_id')
 product = Product.objects.get(id=product_id)
 Cart(user=user ,product = product).save()
 return redirect('/cart') 

@login_required
def show_cart(request):
 if request.user.is_authenticated:
  user = request.user
  cart = Cart.objects.filter(user=user)
  # print(cart)
  amount = 0.0 
  shipping_amount = 70.0
  total_amount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user == user]
  # print(cart_product)
  if cart_product:
   for p in cart_product:
    tempamount = (p.quantity * p.product.discount_price)
    amount += tempamount
    totalamount = amount + shipping_amount
   return render(request, 'app/addtocart.html',{'carts':cart , 'totalamount':totalamount,'amount':amount})
  else:
   return render(request , 'app/emptycart.html')


def plus_cart(request):
 if request.method=="GET":
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity += 1
  c.save()
  amount = 0.0
  shipping_amount = 70.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
    tempamount = (p.quantity * p.product.discount_price)
    amount += tempamount
  data = {
    'quantity':c.quantity,
    'amount':amount,
    'totalamount':amount + shipping_amount
  }
  return JsonResponse(data)
 

def minus_cart(request):
 if request.method=="GET":
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity -= 1
  c.save()
  amount = 0.0
  shipping_amount = 70.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
    tempamount = (p.quantity * p.product.discount_price)
    amount += tempamount
  data = {
    'quantity':c.quantity,
    'amount':amount,
    'totalamount':amount + shipping_amount

  }
  return JsonResponse(data)


def remove_cart(request):
 if request.method=="GET":
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.delete()
  amount = 0.0
  shipping_amount = 70.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
    tempamount = (p.quantity * p.product.discount_price)
    amount += tempamount
  data = {
    'amount':amount,
    'totalamount':amount + shipping_amount

  }
  return JsonResponse(data)





def buy_now(request):
 return render(request, 'app/buynow.html')

@login_required
def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html',{'add':add,'active':'btn-primary'}) 

@login_required
def orders(request):
 op = OrderPLaced.objects.filter(user = request.user)
 return render(request, 'app/orders.html',{'order_placed':op})

def mobile(request,data=None,):
  brands = Product.objects.filter(category="M").values_list('brand',flat=True).distinct()
  print(brands)
  if data==None:
    mobiles = Product.objects.filter(category="M")
  else:
    mobiles =  Product.objects.filter(category="M").filter(brand=data)
  return render(request, 'app/mobile.html',{'mobiles':mobiles , 'brands':brands})
  # if data == None:
  #   mobiles = Product.objects.filter(category="M")
  # elif data == "redmi" or data=="oppo" or data=="redmi":
  #  mobiles =  Product.objects.filter(category="M").filter(brand=data)
  # elif data == 'below':
  #  mobiles =  Product.objects.filter(category="M").filter(discount_price__lt=10000)
  # elif data == 'above':
  #  mobiles =  Product.objects.filter(category="M").filter(discount_price__gt=10000)
def laptop(request,data=None):
 brands = Product.objects.filter(category="L").values_list('brand',flat=True).distinct()
 if data == None:
  laptops = Product.objects.filter(category="L")
 else:
  laptops = Product.objects.filter(category="L").filter(brand = data)
 return render(request , 'app/laptop.html',{'laptops':laptops,'brands':brands})
  

def topwears(request , data=None):
  brands = Product.objects.filter(category="TW").values_list('brand',flat=True).distinct()
  if data == None:
    topwears = Product.objects.filter(category="TW")
  else:
    topwears =  Product.objects.filter(category="TW").filter(brand=data)
  return render(request, 'app/topwears.html',{'topwears':topwears ,'brands':brands})

def bottomwears(request , data=None):
  brands = Product.objects.filter(category="BW").values_list('brand',flat=True).distinct()
  if data == None:
    bottomwears = Product.objects.filter(category="BW")
  else:
    bottomwears = Product.objects.filter(category="BW").filter(brand=data)
  return render(request, 'app/bottomwears.html',{'bottomwears':bottomwears,'brands':brands})


class CustomerRegistrationView(View):
 def get(self , request):
  form = CustomerRegistrationForm()
  return render(request ,'app/customerregistration.html',{'form':form})
 def post(self, request):
  form = CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request,"Congratulations! registered Successfully")
   form.save()
  return render(request , 'app/customerregistration.html',{'form':form})
 
@login_required
def checkout(request):
 user = request.user
 add = Customer.objects.filter(user=user)
 cart_items = Cart.objects.filter(user=user)
 amount = 0.0
 shipping_amount = 70.0
 totalamount = 0
 cart_product = [p for p in Cart.objects.all() if p.user == request.user]
 if cart_product:
  for p in cart_product:
    tempamount = (p.quantity * p.product.discount_price)
    amount += tempamount
  totalamount = amount + shipping_amount
 return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount,'cart_items':cart_items})

@login_required
def payment_done(request):
 user = request.user
 custid = request.GET.get('custid')
 customer = Customer.objects.get(id=custid)
 cart = Cart.objects.filter(user=user)
 for c in cart:
  OrderPLaced(user = user , customer=customer , product=c.product , quantity=c.quantity).save()
  c.delete()
 return redirect('orders')

@method_decorator(login_required , name='dispatch')
class ProfileView(View):
 def get(self , request):
  form = CustomerProfileForm()
  return render(request , 'app/profile.html',{'form':form , 'active':'btn-primary'})
 def post(self , request):
  form = CustomerProfileForm(request.POST)
  if form.is_valid():
    usr = request.user
    name = form.cleaned_data['name']
    locality = form.cleaned_data['locality']
    city = form.cleaned_data['city']
    state = form.cleaned_data['state']
    zipcode = form.cleaned_data['zipcode']
    reg = Customer(user=usr ,name=name , locality=locality , city=city ,state=state , zipcode=zipcode)
    reg.save()
    messages.success(request , "Congretulations Profile upadted successfully!")
  return render(request , 'app/profile.html',{'form':form , 'active':'btn-primary'})


def search(request):
  query = request.GET['query']
  if query:
    topwears = Product.objects.filter(category="TW").filter(title__icontains=query)
    bottomwears = Product.objects.filter(category='BW').filter(title__icontains=query)
    mobiles=Product.objects.filter(category="M").filter(title__icontains=query)
    return render(request , 'app/search.html', {'topwears':topwears , 'bottomwears':bottomwears,'mobiles':mobiles})
  else:
   return render(request,'app/notfount.html')
   
#  return HttpResponse("This is search")