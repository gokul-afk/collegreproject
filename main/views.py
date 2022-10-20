from itertools import product
import os
import datetime
from turtle import goto
from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from main.models import *

# Create your views here.
def home(request):
    return render(request,'home.html')

def men(request,cat):
    p=Products6.objects.filter(category__in=Category6.objects.get(name=cat).get_descendants(include_self=True))
    cal=Products6.objects.filter(category__in=Category6.objects.get(name='men').get_descendants(include_self=False)).order_by('category_id')
    if  request.user.is_authenticated:
        u=UserProfile.objects.get(user_id=request.user.id)
        wishme=Wish.objects.filter(customer_id=u.id)
        context={'pdt':p,'cat':cal,'wishes':wishme}
    else:
        context={'pdt':p,'cat':cal,}
    return render(request,'men.html',context)

def woman(request,cat):
    pt=Products6.objects.filter(category__in=Category6.objects.get(name=cat).get_descendants(include_self=True))
    cat=Products6.objects.filter(category__in=Category6.objects.get(name='women').get_descendants(include_self=False)).order_by('category_id')
    if  request.user.is_authenticated:
        u=UserProfile.objects.get(user_id=request.user.id)
        wishme=Wish.objects.filter(customer_id=u.id)
        context={'pdt':pt,'cat':cat,'wishes':wishme}
    else:
        context={'pdt':pt,'cat':cat,}
    return render(request,'woman.html',context)

def showorders(request):
    u=request.user
    usr=UserProfile.objects.get(user_id=u.id)
    o=Order.objects.filter(customer_id=usr.id)
    wishme=Wish.objects.filter(customer_id=usr.id)
    context={'orders':o,'wishes':wishme}
    return render(request,'Ordered.html',context)

def wishlist(request):
    u=UserProfile.objects.get(user_id=request.user.id)
    wishme=Wish.objects.filter(customer_id=u.id)
    context={'pdt':wishme,'wishes':wishme}
    return render(request,'wishlisted.html',context)


def product_details(request,pk):
    pt=Products6.objects.get(id=pk)
    mi=multimage.objects.filter(product_id=pk)
    sib=Products6.objects.filter(category__in=Category6.objects.get(id=pt.category.id).get_siblings(include_self=True))
    for i in sib:
        print(i.image1.url)
    print(sib)
    context={'pdt':pt,'multi':mi,'sib':sib}
    return render(request,'productdetails.html',context)


def addtocart(request,pk):
    pt=Products6.objects.get(id=pk)
    usr=User.objects.get(username=request.user)
    u=UserProfile.objects.get(user_id=usr.id)
    
    if Cart.objects.filter(customer_id=u.id, product_id=pk).exists():
        o=Cart.objects.get(customer_id=u.id, product_id=pk)
        o.quantity+=1
        o.price=pt.price*o.quantity
        o.save()
    else:
        o=Cart()
        o.product=pt
        o.customer=u
        o.quantity=1
        o.price=pt.price
        o.save()
    return redirect('bag')

def signup(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        adr1=request.POST['adrone']
        adr2=request.POST['adrtwo']
        adr3=request.POST['adrthree']
        uname=request.POST['username']
        password=request.POST['password']
        cpassword=request.POST['cpassword']
        email=request.POST['email']
        gender=request.POST.get('gender')
        mobile=request.POST.get('mobile')

        if password==cpassword:  #  password matching......
            if User.objects.filter(username=uname).exists(): #check Username Already Exists..
                print("Username already Taken..")
                return render(request,'home.html')
            else:
                users=User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=uname,
                    password=password,
                    email=email)
                users.save()
                u=User.objects.get(id=users.id)
                member=UserProfile(user_gender=gender,
                                      user_mobile=mobile,
                                      user=u,
                                      address1 = adr1, 
                                      address2 =adr2,
                                      address3 = adr3,
                                      )
                member.save()
                print("savedd")
                


        else:
            print("Password is not Matching.. ") 
            return render(request,'home.html')
        return render(request,'home.html')
        
    else:
        print("post")
        return render(request,'home.html')

def login(request):
    try:
        if request.method == 'POST':
            try:
                username = request.POST['username']
                password = request.POST['password']
                user = auth.authenticate(username=username, password=password)
                request.session["uid"] = user.id
                if user is not None:
                    auth.login(request, user)
                    return redirect('home')
                else:
                    print('Invalid username or password')
                    return render(request,'home')
            except:
                print( 'main code')
                return render(request, 'home.html')
        else:
            return render(request,'home')
    except:
        print('whole code')
        return render(request,'home')

def bag(request):
    u=request.user
    usr=UserProfile.objects.get(user_id=u.id)
    c=Cart.objects.filter(customer_id=usr.id)
    w=Wish.objects.filter(customer_id=usr.id)
    sum=0
    dc=0
    for i in c:
        sum+=i.price
        dc=149
    tc=sum+dc 
    context={'carts':c,'sum':sum,'tc':tc,'dc':dc,'wishes':w}
    return render(request,'Shoppingbag.html',context)

def logout(request):
    request.session["uid"] = ""
    auth.logout(request)
    return redirect('home')



def order(request):
    u=UserProfile.objects.get(user_id=request.user.id)
    c=Cart.objects.filter(customer_id=u.id)
    for b in c:
        o=Order()
        o.product=Products6.objects.get(id=b.product_id)
        o.customer=u
        o.quantity=b.quantity
        o.price=b.price
        o.address=b.customer.address1+", "+b.customer.address2+", "+b.customer.address3
        o.phone = b.customer.user_mobile
        o.save()
        b.delete()
    return render(request,'ordered.html')

def deletecart(request,pk):

    b=Cart.objects.get(product_id=pk)
    b.delete()
    return redirect((request.META.get('HTTP_REFERER')))

def deleteorder(request,pk):
    b=Order.objects.get(id=pk)
    b.delete()
    return redirect((request.META.get('HTTP_REFERER')))

def wish(request,pk):
    usr=UserProfile.objects.get(user_id=request.user.id)
    if(Wish.objects.filter(customer_id=usr.id,product_id=pk).exists()):
        w=Wish.objects.filter(customer_id=usr.id,product_id=pk)
        w.delete()
    else:
        w=Wish()
        w.product=Products6.objects.get(id=pk)
        w.customer=UserProfile.objects.get(user_id=request.user.id)
        w.save()
    return redirect((request.META.get('HTTP_REFERER')))