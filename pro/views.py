from cmath import isnan
from django.shortcuts import render,redirect
from carts.views import _cart_id
from carts.models import Cart,CartItem
# Create your views here.
from django.contrib import admin
from django.urls import path
from django.urls import reverse_lazy
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from orders.forms import *
from django.contrib.auth.hashers import make_password, check_password
from orders.models import *
from .models import *
from coupons.forms import *
from django.db.models import Sum

import datetime
from .filters import *

from django.http import HttpResponse,HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.views.decorators.cache import never_cache
from django.core.mail import send_mail
import random
from django.conf import settings
import vonage
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView 
from django.views.decorators.cache import cache_control
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.views.generic import ListView,DeleteView,DetailView,UpdateView,CreateView
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.http import HttpResponse
from image_cropping.utils import get_backend

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logi(req):

    if 'kp' in req.session:
        return redirect('admhome')
   

    if req.method =='POST':
        a=req.POST.get('username')
        b=req.POST.get('password')
        u=auth.authenticate(username=a,password=b)
        
        if u is not None:
            
            print(req.user.is_authenticated)
            req.session['kp']=123

             
            return redirect('admhome')
        else:
            messages.error(req, "incorrect username or password") 
            return redirect('adm')
    
    else:
       return render(req,"admlogin.html")
                  
                   
                            
    
   



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def lo(req):
    
          del req.session['kp']
     
          return redirect('uhome')
      

def user_address(request):
    
    
    if request.method=='POST':
        add=request.POST.get('address')
        k=Address(addresssave=add,useradd=request.user)
        k.save()
        return redirect('profile')


    
    return render(request,"store/address.html")

import xlwt

def u_address(request):
    
    
    if request.method=='POST':
        print("hloo")
        add=request.POST.get('address')
        print(add)
        k=Address(addresssave=add,useradd=request.user)
        k.save()
        return HttpResponse("address added")

    else:
         return HttpResponse("failed")
            
def c_address(request):
    
    
    if request.method=='POST':
        print("hloo")
        add=request.POST.get('address')
        print(add)
        check=Address.objects.filter(addresssave=add,useradd=request.user)
        if check:
            messages.error(request,"you have already added this address")
            return redirect("checkout")

        else:    
            k=Address(addresssave=add,useradd=request.user)
            k.save()
            return redirect("checkout")

    return render(request,"store/address.html")


    
    
import math
@cache_control(no_cache=True, must_revalidate=True, no_store=True)

def admhome(re):

    if 'kp' in re.session:
    
        pi=produc.objects.all().distinct('name')
        
        productForm=BannerForm()
        # myFilter=productFilter(re.GET,queryset=p)
        # p=myFilter.qs.
        labels=[]
        data=[]
        order=[]
        stock=[]
        o=OrderProduct.objects.all()
        pay=Payment.objects.all()
        for p in pay:
         print(p.created_at)   
         labels.append(p.user.fname)
         data.append(p.amount_paid)

        for i in pi:
            order.append(i.stock)

        for k in o:
         
        
            stock.append(1)


        s=math.fsum(data)
        t=sum(order)
        y=sum(stock)

        context={'labels':labels,'data':data,'pro':pi,'productForm':productForm,'sum':s,'order':t,'stock':y}
       
        # page = re.GET.get('page', 7)

        # paginator = Paginator(p, 1)
        # try:
        #                 users = paginator.page(page)
        # except PageNotAnInteger:
        #                 users = paginator.page(1)
        # except EmptyPage:
        #                 users = paginator.page(paginator.num_pages)


        
        return render(re,'admhome.html',context)

    else:
        return redirect('adm')     


def admproduct(request):

    if 'kp' in request.session:
       p=produc.objects.all()
       pro=ProductForm()
       productForm=BannerForm()
      
       myFilter=productFilter(request.GET,queryset=p)
       p=myFilter.qs
       page = request.GET.get('page', 7)

       paginator = Paginator(p, 7)
       try:
                       users = paginator.page(page)
       except PageNotAnInteger:
                        users = paginator.page(1)
       except EmptyPage:
                        users = paginator.page(paginator.num_pages)

       return render(request,"store/admproduct.html",{'g':users,'productForm':pro,'b':productForm}) 

    else:
        return redirect('adm')                  


  






def userlog(request):

    # if 'k' in request.session :    
    #     return redirect('uhome')

    if 'ci' in request.session:
        messages.info(request,'registration and phone verification successfull')    

    if 'gt' in request.session:
        messages.info(request, "you are blocked contact admin!!")

    
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        print(username)

        if username == "" and password == "":
            messages.error(request,"please enter credentials")
            return HttpResponseRedirect('/')

        else:

    
        
            user=auth.authenticate(username=username,password=password)
            
            if user  :
                
                
                k=customer.objects.get(username=username)

                if k.status =='True':
                    # request.session['k']=username
                    print('logged in') 
                    if 'k' in request.session or  'gt' in request.session or 'otp' in request.session or 'si' in request.session or 'ci' in request.session:
    
                        request.session.flush()

                    try:
                        
                        cart=Cart.objects.get(cart_id=_cart_id(request)) 
                        i=CartItem.objects.filter(cart=cart).exists()
                        if i:
                            cart_item=CartItem.objects.filter(cart=cart)
                            print(cart_item)
                            for item in cart_item:
                                item.user=user
                                item.save()
                    except:
                        pass       
                    auth.login(request,user)
                    print(request.user.is_authenticated)
                    print(request.user)
                    t=k.id 
                
                    request.session['cusid']=t   
                    return redirect('uhome')

            elif not user:   

                
                messages.info(request, "incorrect username or password") 
     
                return redirect('ulog') 
    else:
        return render(request,"userlog.html")            
           
            

    
            
     
     

def cre(request):
    if request.method == "POST":
        name=request.POST.get('name')
        slug=request.POST.get('slug')
        check=category.objects.filter(category_name=name)
        if check:
            messages.info(request,"Already exists")
            return redirect("cat")

        else:    
            c=category(category_name=name,slug=slug)
            print("huhu")
            c.save()
            return redirect('cat')


def delet(request,id):
    
    c=category.objects.get(id=id)
    pr=produc.objects.filter(cate_id=c)
    if pr:
        messages.info(request,"products of these categories are already added .delete them to proceed")
    else:    
      c.delete()
    return redirect('cat')

class cupd(LoginRequiredMixin,UpdateView):
    model=category
    template_name="catup.html"
    fields='__all__'
    pk_url_kwarg='pk'
    success_url= reverse_lazy("cat")
    login_url='adm'
    redirect_field_name='cupd'

def ban(request):
    productForm=BannerForm()
    if request.method=='POST':
        productForm=BannerForm(request.POST, request.FILES)
        if productForm.is_valid():
            productForm.save()
        return redirect('admhome')
    return render(request,'banner.html',{'productForm':BannerForm})


def _wish_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart
@login_required(login_url="ulog")
def wish_cart(request, product_id):
    #get the product
    # If the user is authenticated
    
    product= produc.objects.get(id=product_id)
    if request.user.is_authenticated:
        try:
            cart= wish.objects.get(cart_id =_wish_id(request))
        except:
            cart = wish.objects.create(
                cart_id=_wish_id(request)
            )
            cart.save()
        try:
            cart_item = wishItem.objects.get(product=product,cart=cart,user=request.user)
            cart_item.quantity += 1 #pressing first time cart button
            cart_item.save()
        except wishItem.DoesNotExist:
            cart_item = wishItem.objects.create(
                product=product,
                quantity=1,
                user=request.user,
                cart=cart,
            )
            cart_item.save()

       
        
            
            



    else:
    
        try:    
                
                cart = wish.objects.get(cart_id=_wish_id(request)) # get the cart using the cart_id present in the session
        except Cart.DoesNotExist:
                
                cart = wish.objects.create( cart_id = _wish_id(request))
                cart.save()

        try: 
        
            cart_item=wishItem.objects.get(product=product,cart=cart)
            cart_item.quantity += 1
            cart_item.save()

        except wishItem.DoesNotExist:
            
            cart_item=wishItem.objects.create(product=product,quantity=1,cart=cart,)
            cart_item.save()

        
    return redirect('wcart')     






       

def wcart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = wishItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = wish.objects.get(cart_id=_wish_id(request))
            cart_items = wishItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass #just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total,
    }
    return render(request,"store/wishlist.html",context)    


def removewcart(request, product_id, cart_item_id):

    product = get_object_or_404(produc, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = wishItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_wish_id(request))
            cart_item = wishItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('wcart')







def remove_wcart_item(request, product_id, cart_item_id):
    product = get_object_or_404(produc, id=product_id)
    if request.user.is_authenticated:
        print(request.user)
        cart_item = wishItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = wish.objects.get(cart_id=_wish_id(request))
        cart_item = wishItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('wcart')








  

       


def filt(request,price,price2):
    products=produc.objects.filter(price__lte=price2,price__gte=price)
    print(price)
    print(price2)
    myFilter=productFilter(request.GET,queryset=products)
    products=myFilter.qs
    paginator = Paginator(products, 3)
    page = request.GET.get('page')
    t=banner.objects.first()
    paged_products = paginator.get_page(page)
    product_count = products.count()

    
    context = {
        'products': paged_products,
        'product_count': product_count,
        'banner':t,
        'myFilter':myFilter,
    }    

    return render(request,"store/filter.html",context)




    

def uhome(request,category_slug=None):

    # if 'k'in re.session or 'otp' in re.session:
    categories = None
    products = None
    
    if category_slug != None:
        categories = get_object_or_404(category, slug=category_slug)
        products = produc.objects.filter(cate_id=categories)
        myFilter=productFilter(request.GET,queryset=products)
        products=myFilter.qs
        paginator = Paginator(products, 8)
        page = request.GET.get('page')
        t=banner.objects.first()
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = produc.objects.all().order_by('id')
        myFilter=productFilter(request.GET,queryset=products)
        products=myFilter.qs

        paginator = Paginator(products, 8)
        t=banner.objects.first()
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
        # if 'prooffer' in request.session:

        #     check=productoffer.objects.filter(id=request.session.get('prooffer'),valid_from__lte=datetime.datetime.now().strftime ("%Y-%m-%d"),valid_to__gte=datetime.datetime.now().strftime ("%Y-%m-%d"),is_active=True)
        #     if check:
        #         for  i in check:
        #             product=produc.objects.get(name=i.productname)
        #             if i.percentage >70:
        #                 pass

        #             else:


        #                 print(i.product.offer)
        #                 print(i.product.price)
                
        #                 product.offer= product.price
        #                 product.price -= product.price * ( i.percentage/100)
        #                 product.save()
        #                 print('success')  

        #     else:
                
        #         print("else")
              
            
        #         for i in check:
            
        #                 product=produc.objects.get(name=i.productname)
        #                 product.offer="None"
        #                 product.save()
        #                 i.is_active=False
        #                 i.save()  

        # if 'c_offer' in request.session:
        #     check=categoryoffer.objects.filter(id=request.session.get('c_offer'),valid_from__lte=datetime.datetime.now().strftime ("%Y-%m-%d"),valid_to__gte=datetime.datetime.now().strftime ("%Y-%m-%d"),is_active=True)
   
        #     if check:
        #         for k in check:
        #             print('if')
        #             c=category.objects.get(category_name=k.categoryname)
        #             p=produc.objects.filter(cate_id=c.id)

        #             for i in p:
        #                 if k.percentage >70:
        #                     pass
        #                 else:
        #                     i.offer=i.price
        #                     i.save()
        #                     print('total price',i.offer)
        #                     print(k.percentage)
        #                     print("type",type(k.percentage))
        #                     kp=int(k.percentage)
        #                     print('kp',kp)
                        
        #                     offer=i.price-(i.price*(kp/100))
        #                     i.price =offer
        #                     i.save()
        #                     print('price after offer',i.price)
        #     else:
        #         for i in check:
        #             print('else')
        #             i.is_active=False
        #             i.save()
                   
        #             l=category.objects.get(category_name=i.categoryname)
        #             print(l)
        #             p=produc.objects.filter(cate_id=l.id)
        #             print(p)
                    
        #         for i in p:
        #             i.offer= "None"
        #             i.save()
        
            


    context = {
        'products': paged_products,
        'product_count': product_count,
        'banner':t,
        'myFilter':myFilter,
    }    




     
    return render(request,'uhome.html',context)

    #  else:
    #     return  redirect('ulog')



    


   
def ulo(r):
    if 'k' in r.session or 'otp' in r.session or 'si' in r.session or 'ci' in r.session or 'cusid' in r.session:
        r.session.flush()
        auth.logout(r)
    return redirect('uhome')      




def sales_report_date(request):
    data = OrderProduct.objects.all()
    if request.method == 'POST':
        if request.POST.get('month'):
            month = request.POST.get('month')
            print(month)
            data = OrderProduct.objects.filter(created_at__icontains=month)
            
            if data:
                if SalesReport.objects.all():
                    SalesReport.objects.all().delete()
                    for i in data:
                        sales = SalesReport()
                        sales.productName = i.product.name
                        sales.categoryName = i.product.cate_id.category_name
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'sales_report_.html',context)
                else:
                    for i in data:
                        sales = SalesReport()
                        sales.productName = i.product.name
                        sales.categoryName = i.product.cate_id.category_name
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'sales_report_.html',context)
            else:
                messages.warning(request,"Nothing Found!!")
        if request.POST.get('date'):
            date = request.POST.get('date')
            print("0,",date)
            
            date_check = OrderProduct.objects.filter(created_at__icontains=date)
            print(date_check)
            if date_check:
                if SalesReport.objects.all():
                    SalesReport.objects.all().delete()
            
                    for i in date_check:
                        sales = SalesReport()
                        sales.productName = i.product.name
                        sales.categoryName = i.product.cate_id.category_name
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'sales_report_.html',context)
                else:
                    for i in date_check:
                        sales = SalesReport()
                        sales.productName = i.product.name
                        sales.categoryName = i.product.cate_id.category_name
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'sales_report_.html',context)
            else:
                messages.warning(request,"Nothing Found!!")
        if request.POST.get('date1'):
            date1 = request.POST.get('date1')
            date2 = request.POST.get('date2')
            data_range = OrderProduct.objects.filter(created_at__gte=date1,created_at__lte=date2)
            if data_range:
                if SalesReport.objects.all():
                    SalesReport.objects.all().delete()
            
                    for i in data_range:
                        sales = SalesReport()
                        sales.productName = i.product.name
                        sales.categoryName = i.product.cate_id.category_name
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'sales_report_.html',context)
                else:
                    for i in data_range:
                        sales = SalesReport()
                        sales.productName = i.product.name
                        sales.categoryName = i.product.cate_id.category_name
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'sales_report_.html',context)
            else:
                messages.warning(request,"Nothing Found!!")
    if data:
        if SalesReport.objects.all():
            SalesReport.objects.all().delete()
            for i in data:
                sales = SalesReport()
                sales.productName = i.product.name
                sales.categoryName = i.product.cate_id.category_name
                sales.date = i.created_at
                sales.quantity = i.quantity
                sales.productPrice = i.product_price
                sales.save()
            sales = SalesReport.objects.all()
            total = SalesReport.objects.all().aggregate(Sum('productPrice'))
            context = { 'sales':sales,'total':total['productPrice__sum']}
            return render(request,'sales_report_.html',context)

        else:
            for i in data:
                sales = SalesReport()
                sales.productName = i.product.name
                sales.categoryName = i.product.cate_id.category_name
                sales.date = i.created_at
                sales.quantity = i.quantity
                sales.productPrice = i.product_price
                sales.save()
            sales = SalesReport.objects.all()
            total = SalesReport.objects.all().aggregate(Sum('productPrice'))
            context = { 'sales':sales,'total':total['productPrice__sum']}
            return render(request,'sales_report_.html',context)
        
    else:
        messages.warning(request,"Nothing Found!!")
    
    return render(request,'sales_report_.html')

def export_to_excel(request):
    response = HttpResponse(content_type = 'application/ms-excel')
    response['content-Disposition'] = 'attachment; filename="sales.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sales Report') #this will generate a file named as sales Report

     # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Product Name','Category','Price','Quantity', ]

    for col_num in range(len(columns)):
        # at 0 row 0 column
        ws.write(row_num, col_num, columns[col_num], font_style)

    
    font_style = xlwt.XFStyle()
    total = 0

    rows = SalesReport.objects.values_list(
        'productName','categoryName', 'productPrice', 'quantity')
    for row in rows:
        total +=row[2]
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    row_num += 1
    col_num +=1
    ws.write(row_num,col_num,total,font_style)

    wb.save(response)

    return response



def export_to_pdf(request):
    prod = produc.objects.all()
    order_count = []
    # for i in prod:
    #     count = SalesReport.objects.filter(product_id=i.id).count()
    #     order_count.append(count)
    #     total_sales = i.price*count
    sales = SalesReport.objects.all()
    total_sales = SalesReport.objects.all().aggregate(Sum('productPrice'))



    template_path = 'sales_pdf.html'
    context = {
        'brand_name':prod,
        'order_count':sales,
        'total_amount':total_sales['productPrice__sum'],
    }
    
    # csv file can also be generated using content_type='application/csv
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response


from django.utils.crypto import get_random_string
def signup(request):
   

        if 'si' in request.session:
            messages.error(request,"verification failed ...enter correct phone number!!!")

        if 'r'in request.session:
             messages.info(request,"please sign up first then only you can use otp metthod!!!")

        if request.method=='POST':
                fname = request.POST.get('fname')
                lname = request.POST.get('lname')
                username = request.POST.get('username')
                password = request.POST.get('password')
                email = request.POST.get('email')
                phone = request.POST.get('phone')
                Address= request.POST.get('Address')
                referral=request.POST.get('referral')
                

                if customer.objects.filter(email=email).exists():
                    messages.info(request,'Email already exist')
                    return redirect('signup')

                
                elif customer.objects.filter(username=username).exists():
                    messages.info(request,'Username is not available')
                    return redirect('signup')

                elif fname==''or lname==''or username==''or password =='' or email== ''or phone =='':
                    messages.info(request,'fill empty fields')
                    return redirect('signup')


                else:    

                  s=customer.objects.create_user(fname=fname,lname=lname,username=username,password=password,email=email,address=Address,referral=get_random_string(length=32))
                  s.phone=phone
                  s.save()

                  w=Wallet(user_e=email)
                  w.w_amount=0

                  w.save()
                  print("wallet created",w)

                  if referral:
                    kp=customer.objects.filter(referral=referral)

                    if kp:
                        print("referral exists")
                        for i in kp:
                            g=Wallet.objects.get(user_e=i.email)
                            g.w_amount = 0
                            g.save()
                            g.w_amount +=100
                            g.save()
                        print('success')
                        w.w_amount+=40
                        w.save()
                        request.session['wallet']=1234567

                    else:
                        print("failed") 

                  else:
                    # print("invalid referral")
                    # messages.info(request,"invalid referral")   
                    pass    
                  
                  if 'phone' in request.session:
                    return redirect('emai')
                  else:
                    return redirect('ulog')  
                #   client = vonage.Client(key="9fd7e95f", secret="2V2n91tcD3d52kU7")
                #   verify = vonage.Verify(client)
                #   response = verify.start_verification(number="918590124080", brand="AcmeInc")

                #   if response["status"] == "0":
                #           print("Started verification request_id is %s" % (response["request_id"]))
                #           request.session['phone']=response["request_id"]
                #           return redirect('verifyi')
                #   else:
                #         print("Error: %s" % response["error_text"])

                  

             
                
                
        

    
   



        return render(request,"usignup.html")

def index(request):
    g=produc.objects.all()[:3]
   
    h=banner.objects.all()
    context={'pro':g,'ban':h}
    return render(request,"index.html",context)




def verifyi(re):
     if re.method=='POST':
        code=re.POST.get('emaill')
        k=re.session.get('phone')
        # client = vonage.Client(key="9fd7e95f", secret="2V2n91tcD3d52kU7")
        # verify = vonage.Verify(client)

        # response = verify.check(k, code=code)

        # if response["status"] == "0":
        #     print("Verification successful, event_id is %s" % (response["event_id"]))
        #     re.session['ci']=123
        #     return redirect('ulog')
           
        # else:
        #     print("Error: %s" % response["error_text"])
        #     re.session['si']=456
        #     return redirect('signup')


     return render(re,"phoneverify.html")           

def  emai(re):
 
    if re.method=='POST':
        email=re.POST.get('emaill')
        f =customer.objects.filter(phone=email) 
        if f:
            k=customer.objects.get(phone=email)
            if k.status=='True': 
                  client = vonage.Client(key="9fd7e95f", secret="2V2n91tcD3d52kU7")
                  verify = vonage.Verify(client)
                  response = verify.start_verification(number="918590124080", brand="AcmeInc")

                  if response["status"] == "0":
                          print("Started verification request_id is %s" % (response["request_id"]))
                          re.session['phone']=response["request_id"]
                          re.session['email']=email
                          return redirect('otp')
                  else:
                        print("Error: %s" % response["error_text"])

                # otp=str(random.randint(1000,9999))
                # print(otp,email)
                # subject = 'welcome to GFG world'
                # message = 'your otp is '+otp
                # email_from = settings.EMAIL_HOST_USER
                # recipient_list = [email]
                # send_mail( subject, message, email_from, recipient_list )
                # re.session['otp']=otp
                
            else:
                re.session['s']=234
                messages.error(re,"you are blocked")
                return redirect('emai')
                 
        else:
            re.session['r']=123
            return redirect("signup")          
    return render(re,"email.html")     


def emailre(re):
    if re.method=='POST':
        email=re.POST.get('emaill')    
        otp=str(random.randint(1000,9999))
        print(otp,email)
        subject = 'welcome to GFG world'
        message = 'your new otp is '+otp
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail( subject, message, email_from, recipient_list )
        re.session['otp2']=otp
    
        return redirect('resend')
    return render(re,"email.html")     

def resend(re):
     otps=re.session.get('otp2')
     print(otps)
     if re.method=='POST':
        t=re.POST.get('otp')
        print(t)
        if otps==t:
            
            return redirect('uhome')

        else:
            messages.error(re,"invalid otp")
            return redirect('resend')    
    
     


     return render(re,'resend.html')    
   
    
def  otp(re):
    if re.method =='POST':
        t=re.POST.get('otp')
        k=re.session.get('phone')
        client = vonage.Client(key="9fd7e95f", secret="2V2n91tcD3d52kU7")
        verify = vonage.Verify(client)

        response = verify.check(k, code=t)

        if response["status"] == "0":
            print("Verification successful, event_id is %s" % (response["event_id"]))
            re.session['ci']=123
            phone=re.session.get('email')
           

            a=customer.objects.get(phone=phone)
            print(a.username)
            print(a.password)
            
            
            
            print('entered')
            auth.login(re,a)
            re.session['cusid']=1233 
            return redirect('uhome')
             
        else:
            print("Error: %s" % response["error_text"])
            re.session['si']=456
            return redirect('signup')


    #  otps=re.session.get('otp')
    #  print(otps)
    #  if re.method=='POST':
    #     t=re.POST.get('otp')
    #     print(t)
    #     if otps==t:
            
    #         return redirect('uhome')

    #     else:
    #         messages.error(re,"invalid otp")
    #         return redirect('otp')    
    
    return render(re,"otp.html") 

def orderview(request):
        
        orders=OrderProduct.objects.all().order_by('id')

   
        pf=BannerForm()
    
        page = request.GET.get('page', 1)

        paginator = Paginator(orders, 7)
        try:
                            users = paginator.page(page)
        except PageNotAnInteger:
                            users = paginator.page(1)
        except EmptyPage:
                            users = paginator.page(paginator.num_pages)
        return render(request,'store/admorders.html',{'data':users,'productForm':pf}) 

def ret(request,id):

    o=OrderProduct.objects.get(id=id)
    o.returned="True"
    o.save() 
    messages.info(request,"info has been send to admin")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



        


        

def update_view(request,id):
    order=OrderProduct.objects.get(id=id)
    orderForm=OForm(instance=order)
    if request.method=='POST':
        print('l')
        orderForm=OForm(request.POST,instance=order)
        if orderForm.is_valid():
            OForm.save()
            return redirect('orderview')
    return render(request,'store/update_order.html',{'orderForm':orderForm})
    







# @login_required(login_url='adm')
def admin_add_product_view(request):
    
    productForm=ProductForm()
    p=produc()

    
    if request.method=='POST':
        productForm=ProductForm(request.POST, request.FILES)
        if productForm.is_valid():
            productForm.save()
          
 
        return redirect('admproduct') 
     

       
    return render(request,'pcreate.html',{'productForm':productForm,'prod':p})


# @login_required(login_url='adm')
def update_product_view(request,pk):
    product=produc.objects.get(id=pk)
    
    productForm=ProductForm(instance=product)
    if request.method=='POST':
        print("post")
        productForm=ProductForm(request.POST,request.FILES,instance=product)
        if productForm.is_valid():
            productForm.save()
            print("updated")
            
            return redirect('admproduct')
    return render(request,'pupdate.html',{'productForm':productForm})

def update_view(request,id,t,k):
    p=produc.objects.get(id=id)
    print(p)
    o=Order.objects.get(id=t)
    print(o)
    orde=OrderProduct.objects.get(id=k)
    print(orde)
    orderForm=OForm(instance=orde)
    if request.method=='POST':
        print('l')
        orderForm=OForm(request.POST,instance=orde)
        if orderForm.is_valid():
            orderForm.save()
            return redirect('orderview')
    return render(request,'store/update_order.html',{'orderForm':orderForm})

def delete_order(request,id):
    order=OrderProduct.objects.get(id=id)
    order.delete()
    return redirect('orderview')



def profile(request):
    orders=OrderProduct.objects.all()
    a=Address.objects.filter(useradd=request.user)
    
   
    print(request.user)
    k=customer.objects.get(email=request.user)
    print(k.id)
    
    w=Wallet.objects.get(user_e=request.user)
    


    

    return render(request,"profile.html",{'data':orders,'address':a,'user':k,'wallet':w}) 



def editprofile(request,user_id):
    if request.method == "POST":
        f=request.POST.get('f')
        l=request.POST.get('l')
        e=request.POST.get('e')
        p=request.POST.get('p')
        a=request.POST.get('a')
        k=customer.objects.get(id=user_id)
        k.fname= f
        k.lname= l
        k.email=  e
        k.phone=  p
        k.address=a
        k.save()
        messages.info(request,"profile edited successfully")
        return redirect('profile')

def userorder(request):
    orders=OrderProduct.objects.all().order_by("id")
    
    page = request.GET.get('page', 1)

    paginator = Paginator(orders, 7)
    try:
                        users = paginator.page(page)
    except PageNotAnInteger:
                        users = paginator.page(1)
    except EmptyPage:
                        users = paginator.page(paginator.num_pages)

    context={'orders':users}                    

    return render(request,"store/orders.html",context)        


def changepass(request,user_id):
        print('hello')

        
    
        if request.method == 'POST':    
            u=customer.objects.get(id=user_id)
            print(u.password)
            

            l=request.POST.get('change')
            print(l)
            hashed_pwd = make_password(l)
            print(hashed_pwd)
            t= check_password(l,hashed_pwd)
            print(t)
            if request.user.check_password(l):
                
                print(u.password)
                messages.error(request, "Oops..its your old password!!!")
                print("same password")
                return redirect('profile')
                
                
            else:
                u.password=hashed_pwd
                u.save()
                print(u.password)
                auth.logout(request)
                messages.info(request,"login with new password")
                print("different password")
                return HttpResponseRedirect('/')
                    


def adcancel(request,id):
    a=Address.objects.get(id=id)
    a.delete()
    return redirect('profile')




def user_delete_order(request,pk):
    order=OrderProduct.objects.get(id=pk)
    order.status="cancelled"
    order.save()
    return redirect('userorder')


def checking(request):
    return HttpResponse('success')


def plus(request,product_id):
     if request.user.is_authenticated:

        cart_id = product_id
        # print(cart_id)


        cart_ite = CartItem.objects.get(id = cart_id)
        cart_ite.quantity += 1
        cart_ite.save()

        cart_q = cart_ite.quantity
        print(cart_q, "cart quantity")
        

        return HttpResponse(cart_q)
     



def cat(re):

 if 'kp' in re.session:   

    ii=category.objects.all()
    page = re.GET.get('page', 1)
    c=categoryForm()
    productForm=BannerForm()

    paginator = Paginator(ii, 7)
    try:
                        users = paginator.page(page)
    except PageNotAnInteger:
                        users = paginator.page(1)
    except EmptyPage:
                        users = paginator.page(paginator.num_pages)

    return render(re,"category.html",{'s':users,'category':c,'  productForm':  productForm}) 

 else:
    return redirect('adm')    

    




def productdelete(request,ki):
  pro_delete=produc.objects.get(id=ki)
  pro_delete.delete()
  messages.info(request,"product deleted from inventory")
  return redirect("admproduct")

     
    #  login_url='adm'
    #  redirect_field_name='dele'

class detail(DetailView):
    model=produc
    template_name='detailview.html'
    pk_url_kwarg='pk'
 
    def get(self,re,pk):
        prod=produc.objects.get(id=pk)
        return render(re,'detailview.html',{'h':prod})

class orderdetail(DetailView):
    model=OrderProduct
    template_name='store/orderdetail.html'
    pk_url_kwarg='pk'

    def get(self,re,pk):
        j=OrderProduct.objects.get(id=pk)
        return render(re,'store/orderdetail.html',{'h':j})


import io
from xhtml2pdf import pisa

from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
   
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

   

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response

def download(request,productID):
    v=OrderProduct.objects.get(id=productID)
    mydict={
        
        'customerName':v.user.fname,
        'customerEmail':v.user.email,
        'customerMobile':v.user.phone,
        'shipmentAddress':v.order.address_line_1,
        'orderStatus':v.status,
        'productimage':v.product.img,

        'productName':v.product.name,
    
        'productPrice':v.product.price,
        'productDescription':v.product.description,


    }
     
    return render_to_pdf('store/download.html',mydict)







              

def admuser(req):

  if 'kp' in req.session:  
        if req.method =='POST':
                s=req.POST['search']
                if s is None:
                    productForm=BannerForm()
                    a=customer.objects.all().order_by('id')
                    page = req.GET.get('page', 1)

                    paginator = Paginator(a, 7)
                    try:
                            users = paginator.page(page)
                    except PageNotAnInteger:
                            users = paginator.page(1)
                    except EmptyPage:
                            users = paginator.page(paginator.num_pages)
                    return render(req,'admuser.html',{'h':users,'productForm':productForm})
                else:
                    a=customer.objects.filter(fname__icontains=s).order_by('id')
                    productForm=BannerForm()
                    page = req.GET.get('page', 1)

                    paginator = Paginator(a, 3)
                    try:
                            users = paginator.page(page)
                    except PageNotAnInteger:
                            users = paginator.page(1)
                    except EmptyPage:
                            users = paginator.page(paginator.num_pages)


                    return render(req,'admuser.html',{'h':users,'productForm':productForm})
        else:
                a=customer.objects.all().order_by('id')
                productForm=BannerForm()
                page = req.GET.get('page', 1)

                paginator = Paginator(a, 7)
                try:
                            users = paginator.page(page)
                except PageNotAnInteger:
                            users = paginator.page(1)
                except EmptyPage:
                            users = paginator.page(paginator.num_pages)
                return render(req,"admuser.html",{'h':users,'productForm':productForm})
  else:
        return redirect('adm')




def block(re,pk):
    k=customer.objects.get(id=pk)
    if k.status =='True':

        k.status='false'
        k.save()
    else:
        k.status='True'
        k.save()
        

    r=customer.objects.all().order_by("id")
    return render(re,"admuser.html",{'h':r})    
 

           
      
    
    
    
    









