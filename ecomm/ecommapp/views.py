from django.shortcuts import render,HttpResponse
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import redirect
from ecommapp.models import product,Cart,order
from django.db.models import Q
import random
import razorpay


# Create your views here.
def home(request):
    context={}
    context['name']="johan"
    context['age']=8
    context['x']=10
    context['gender']='male'
    context['product']=[
        {'id':1,'name':'samsung','cat':'mobile','price':20000},
        {'id':2,'name':'shoes','cat':'shoes','price':200},
        {'id':3,'name':'jeans','cat':'clothing','price':2340},
        {'id':4,'name':'cooler','cat':'electronics','price':1500},
    ]

    if context['age']>context['x']:
        res='age is greatest'
    else:
        res="x is greatest"

   
    return render(request,'home.html',context)
def about(request):
    return HttpResponse("this is about page")
def contact(request,a):
    
    print("a",a)
    print(type(a))
    return HttpResponse("this is contact page")

#class based views
class simpleview(View):
    def get(self,request):
        return HttpResponse("hello from simple view")
    
def index(request):
    #userid=request.user.id
    #print("id logged in user:",userid)
    context={}
    p=product.objects.filter(is_active=True)
    print(p)
    print(p[0])
    print(p[0].name)
    print(p[0].price)
    print(p[1])
    print(p[1].price)
    print(p[1].pdetails)
    context['products']=p

    return render(request,'index.html',context)
def catfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(category=cv)
    p=product.objects.filter(q1 & q2)
    print(p)
    context={}
    context['products']=p
    
    return render(request,'index.html',context)
def sort(request,sv):
    if sv=='0':
        col='price'
    else:
        col='-price'
    p=product.objects.filter(is_active=True).order_by(col)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def range(request):
    min=request.GET['min']
    max=request.GET['max']
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=True)
    p=product.objects.filter(q1&q2&q3)
    #print(p)
    context={}
    context['products']=p
    return render(request,'index.html',context)


def user_login(request):
    context={}
    if request.method =="POST":
        u =request.POST['uname']
        p =request.POST['pass']
        print(u)
        print(p)
        if u=="" or p=="":
            context["errmsg"]='feild cannot be empty'
            return render(request,'login.html',context)
        else:
            a=authenticate(username=u,password=p)
            #print(a)
            #print(a.username)
            #print(a.is_superuser)
            if a is not None:
                login(request,a)
                return redirect('/index')
            else:
                context['errmsg']='invalid username nd password'
                return render(request,'login.html')
                #return HttpResponse("else part")
    
    else:
        return render(request,'login.html')
def user_logout(request):
    logout(request)
    return redirect('/index')
def user_register(request):
    context={}
    if request.method =="POST":
        u =request.POST['uname']
        p =request.POST['pass']
        cp =request.POST['cpass']
        print(u)
        print(p)
        print(cp)
        if u==""or p=="" or cp=="":
            context["errmsg"]="Feild cannot be empty"
            return render(request,'register.html',context)
        elif p!=cp:
            context["errmsg"]="password dont match"
            return render(request,'register.html',context)
        else:
            try:
                 u = User.objects.create(username=u,email=u)
                 u.set_password(p)
                 u.save()
                 context['success']='user created succesfully'
                 return render(request,'register.html',context)
            except Exception:
                context['errmsg']="user with same user name already exist"
                return render(request,'register.html',context)
        u = User.objects.create(username=u,email=u)
        u.set_password(p)
        u.save()
        return HttpResponse("data feteched succesfully")
    return render(request,"register.html")
def place_order(request):
     userid=request.user.id
     c=Cart.objects.filter(uid=userid)
     oid=random.randrange(1000,9999)
     print("orderid:",oid)
     for x in c:
         o=order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
         o.save()
         x.delete()
     orders=order.objects.filter(uid=request.user.id)
     s=0
     n=len(c)

     for x in orders:
       #print(x)
       #print(x.pid.price)
       s=s+x.pid.price*x.qty
       n=n+x.qty
     context={}
     context["products"]=orders
     context['total']=s
     context['np']=n    
     return render(request,'place_order.html',context)
     #return HttpResponse("data ")
def pd(request,pid):
    p=product.objects.filter(id=pid)
    print(p)
    context={}
    context['products']=p
    return render(request,"product_detail.html",context)
def addtocart(request,pid):
    if request.user.is_authenticated:
        u=User.objects.filter(id=request.user.id)
        print(u)
        p=product.objects.filter(id=pid)
        print(p)
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1&q2)
        print(c)
        n=len(c)
        print("length:",n)
        context={}
        context['products']=p
        if n==1:
            context['msg']='already exist in cart!!'
            return render(request,'product_detail.html',context)
        else:

            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            #context={}
            #context['products']=p
            context['success']='product added succesfully to cart !!'
            return render(request,'product_detail.html',context)
    else:
        return redirect('/login')
    
def cart(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    print(c)
    #print(c[0])
    #print(c[0].uid.username)
    #print(c[0].uid.email)
    #print(c[0].pid)
    #print(c[0].pid.name)
    #print(c[0].pid.price)
    s=0
    n=len(c)
    for x in c:
        print(x)
        print(x.pid.price)
        s=s+x.pid.price*x.qty
    context={}
    context["products"]=c
    context['total']=s
    context['np']=n
    return render(request,"cart.html",context)
def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/cart')
def updateqty(request,qv,cid):
    context={}
    c=Cart.objects.filter(id=cid)
    n=0
    for x in c:
          print(x)
          n=n+x.qty
    context['totalqty']=n
    if qv=='1':
        t=c[0].qty+1
        c.update(qty=t)
    else:
        if c[0].qty>1:
             t=c[0].qty-1
             c.update(qty=t)
    
   
    return redirect('/cart',context)

def makepayment(request):
    orders=order.objects.filter(uid=request.user.id)
    s=0
    for x in orders:
        s=s+x.pid.price*x.qty
        oid=x.order_id
    client = razorpay.Client(auth=("rzp_test_60IRWWu3XqumIC", "wdSfdkMg7WJrZzz5amb1PaSi"))
    data = { "amount": s*100, "currency": "INR", "receipt": "oid" }
    payment = client.order.create(data=data)
    context={}
    context['data']=payment
    return render(request,'pay.html',context)
        


