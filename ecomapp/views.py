from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from ecomapp.models import Product,Cart,Order
from django.db.models import Q
import razorpay
from django.core.mail import send_mail

# Create your views here.
def product(request):
    #print(request.user.id)
    p=Product.objects.filter(is_active=True)
    context={}
    context['data']=p
    return render(request,'index.html',context)

def register(request):
    context={}
    if request.method=='GET':
        return render(request,'register.html')
    else:
        un=request.POST['uname']
        ue=request.POST['uemail']
        up=request.POST['upass']
        ucp=request.POST['ucpass']

        '''print(un)
        print(ue)
        print(up)
        print(ucp)'''

        if un=="" or ue=="" or up=="" or ucp=="":
            #print("Field cannot be blank")
            context['errmsg']='Field cannot be blank'
        elif up!=ucp:
            #print("Password does not match!")
            context['errmsg']='Password does not match!s'
        elif len(up)<8:
            #print("Password should be greater than 8 characters")
            context['errmsg']='Password should be greater than 8 characters'
        else:
            u=User.objects.create(username=un,email=ue)
            u.set_password(up)
            u.save()
            #return HttpResponse("Registered successfully!")
            context['success']="Registered successfully!"
        return render(request,'register.html',context)

def user_login(request):
    context={}
    if request.method=="GET":
        return render(request,'login.html')
    else:
        un=request.POST['uname']
        up=request.POST['upass']

        '''print(un)
        print(up)'''
        u=authenticate(username=un,password=up)
        print(up)
        if u==None:
            #print("Invalid Credentials")
            context['errmsg']="Invalid Credentials"
            return render(request,'login.html',context)
        else:
            login(request,u)
            return redirect('/product')
            #print("user login successfully!")


        #return HttpResponse("Credential Checked!")

def user_logout(request):
    logout(request)
    return redirect('/product')

def catfilter(request,cv):
    print(cv)
    q1=Q(cat=cv)
    q2=Q(is_active=True)

    p=Product.objects.filter(q1 & q2)
    #print(p)
    context={}
    context['data']=p
    return render(request,'index.html',context)

def sort(request,sv):
    #print(sv)
    if sv=='1':
        #p=Product.objects.order_by('-price').filter(is_active=True)
        t='-price'
    else:
        t='price'
        #p=Product.objects.order_by('price').filter(is_active=True)
    p=Product.objects.order_by(t).filter(is_active=True)
    context={}
    context['data']=p
    return render(request,'index.html',context)

def pricefilter(request):
    mn=request.GET['min']
    mx=request.GET['max']
    #print(mn,' & ',mx)
    q1=Q(price__gte=mn)
    q2=Q(price__lte=mx)
    p=Product.objects.filter(q1 & q2 & q3)
    context={}
    context['data']=p
    return render(request,'index.html',context)

def search(request):
    s=request.GET['find']
    #print(s)
    n=Product.objects.filter(name__icontains=s)
    pd=Product.objects.filter(pdetail__icontains=s)

    all=n.union(pd)
    context={}
    if len(all)==0:
        context['errmsg']='Product not found'
        return render(request,'index.html',context)
    else:
        context['data']=all
        return render(request,'index.html',context)

def product_detail(request,pid):
    # print(pid)
    p=Product.objects.filter(id=pid)
    context={}
    context['data']=p
    return render(request,'product_detail.html',context)
def addtocart(request,pid_id):
    # print("Product id is:",pid)
    # print("user id is:",request.user.id)
    context={}
    if request.user.is_authenticated:
        # print("User is logged in")
        u=User.objects.filter(id=request.user.id)
        p=Product.objects.filter(id=pid_id)
        q1=Q(uid_id=u[0])
        q2=Q(pid_id=p[0])
        c=Cart.objects.filter(q1 & q2)
        context['data']=p

        if len(c)!=0:
            context['errmsg']='Product already exists!!'
            return render(request,'product_detail.html',context)
        else:
            c=Cart.objects.create(uid_id=u[0],pid_id=p[0])
            c.save()
            context['success']="Product added successfully"
            return render(request,'product_detail.html',context)
    else:
        return redirect('login')
        return render(request,'cart.html',)
    #print("Not logged in")
    # return HttpResponse("Fetched")

def viewcart(request):
    c=Cart.objects.filter(uid_id=request.user.id)
    #print(c)
    context={}
    context['data']=c
    s=0
    for i in c:
        s=s + i.pid_id.price * i.qty  #s=s+i
    context['total']=s
    context['n']=len(c)
    return render(request,'cart.html',context)

def updateqty(request,x,cid):
    c=Cart.objects.filter(id=cid)
    q=c[0].qty
    if x=='1':
        q=q+1
    elif q>1:
        q=q-1
    c.update(qty=q)
    return redirect('/cart')

def removecart(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/cart')

def placeorder(request):
    c=Cart.objects.filter(uid_id=request.user.id)
    #print(c)
    context={}
    context['data']=c

    for i in c:
        a=i.pid_id.price*i.qty
        o=Order.objects.create(uid_id=i.uid_id,pid_id=i.pid_id,qty=i.qty,amt=a)
        o.save()
        i.delete()
    return redirect('/fetchorder')
    '''
    s=0
    for i in c:
        s=s + i.pid_id.price * i.qty  #s=s+i
    context['total']=s
    context['n']=len(c)
    return render(request,'placeorder.html',context)'''

def fetchorder(request):
    o=Order.objects.filter(uid_id=request.user.id)
    context={}
    context['data']=o
    s=0
    for i in o:
        s= s + i.amt
    context['total']=s
    context['n']=len(o)

    return render(request,'placeorder.html',context)

def makepayment(request):
    client = razorpay.Client(auth=("rzp_test_ZQahsKFvhXL0tN", "LREc4l4GrJ9WyNbXuQj2uzMl"))

    o=Order.objects.filter(uid_id=request.user.id)
    s=0
    for i in o:
        s= s + i.amt
               

    data = { "amount": s*100, "currency": "INR", "receipt": "order_rcptid_11" }
    payment = client.order.create(data=data)
    # print(payment)
    context={}
    context['payment']=payment
    return render(request,'pay.html',context)

def success(request):
    u=User.objects.filter(id=request.user.id)
    to=[u[0].email]
    sub='E-Shopping402 Order Status'
    frm='samarpatil0793@gmail.com'
    msg="Order Placed Successfully"
    send_mail(sub,msg,frm,to,fail_silently=False)

    return render(request,'success.html')