from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Car,Bid
from .forms import CarForm,BidForm,RegisterForm

def home(request):
    cars=Car.objects.all()
    return render(request,"home.html",{"cars":cars})

def register_view(request):
    form=RegisterForm(request.POST or None)
    if form.is_valid():
        user=form.save()
        login(request,user)
        return redirect("home")
    return render(request,"register.html",{"form":form})

def login_view(request):
    if request.method=="POST":
        u=request.POST.get("username")
        p=request.POST.get("password")
        user=authenticate(request,username=u,password=p)
        if user:
            login(request,user)
            return redirect("home")
    return render(request,"login.html")

def logout_view(request):
    logout(request)
    return redirect("home")

@login_required
def add_car(request):
    form=CarForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        car=form.save(commit=False)
        car.created_by=request.user
        car.save()
        return redirect("home")
    return render(request,"add_car.html",{"form":form})

def car_detail(request,id):
    car=get_object_or_404(Car,id=id)
    bids=car.bids.order_by('-amount')
    form=BidForm(request.POST or None)

    if request.method=="POST" and request.user.is_authenticated:
        amount=float(request.POST.get("amount"))
        if amount<=float(car.highest_bid()):
            messages.error(request,"Bid must be higher!")
        else:
            Bid.objects.create(car=car,user=request.user,amount=amount)
            return redirect("detail",id=id)

    return render(request,"detail.html",{"car":car,"bids":bids,"form":form})




from django.http import JsonResponse

def highest_bid_api(request, id):
    car = Car.objects.get(id=id)
    return JsonResponse({
        "highest_bid": car.highest_bid()
    })