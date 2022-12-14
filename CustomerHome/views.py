from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from CustomerHome.models import Customer
from Owner.models import Owner

from Clothes.models import Clothes
from RentClothes.models import RentClothes

from datetime import datetime
from datetime import date

isLogin = False
isLogout = False

# Create your views here.
def index(request):
    global isLogin
    global isLogout

    if('user_email' in request.session):
        email = request.session.get('user_email')

        result_customer = Customer.objects.filter(customer_email=email)
        result_owner = Owner.objects.filter(Owner_email=email)

        if result_customer.exists():
            request.session['user_email'] = email
            isLogin = True
            return redirect('/Home/')
        elif result_owner.exists():
            request.session['user_email'] = email
            isLogin = True
            return redirect('/Owner/')
        return redirect('/Home/')

    Clothes = Clothes.objects.all()
    if('user_email' not in request.session and isLogout):
        isLogin = False
        isLogout = False
        Message = "Successfully Logged Out!!"
        return render(request,'index.html',{'Message':Message,'Clothes':Clothes})
    return render(request,'index.html',{'Clothes':Clothes})

def signin(request):
    return render(request,'SignIn.html')

def register(request):
    return render(request,'register.html')

def LoginAuthentication(request):
    global isLogin
    login_email=request.POST.get('login_email','')
    login_password=request.POST.get('login_password','')
    # customer = Customer.objects.all()

    result_customer = Customer.objects.filter(customer_email=login_email,customer_password=login_password)
    result_owner = Owner.objects.filter(Owner_email=login_email,Owner_password=login_password)
   

    if result_customer.exists():
        request.session['user_email'] = login_email
        isLogin = True
        return redirect('/Home/')
    elif result_owner.exists():
        request.session['user_email'] = login_email
        isLogin = True
        return redirect('/Owner/')
    
    else:
        Message = "Invalid Email or password!!"
        return render(request,'SignIn.html',{'Message':Message})

def RegisterCustomer(request):
    global isLogin

    customer_firstname=request.POST.get('customer_firstname','')
    customer_lastname=request.POST.get('customer_lastname','')
    customer_dob=request.POST.get('customer_dob','')
    customer_gender=request.POST.get('customer_gender','')
    customer_mobileno=request.POST.get('customer_mobileno','')
    customer_email=request.POST.get('customer_email','')
    customer_password=request.POST.get('customer_password','')
    customer_address=request.POST.get('customer_address','')
    customer_city=request.POST.get('customer_city','')
    customer_state=request.POST.get('customer_state','')
    customer_country=request.POST.get('customer_country','')
    customer_pincode=request.POST.get('customer_pincode','')
    
    result_customer = Customer.objects.filter(customer_email=customer_email)
    result_owner = Owner.objects.filter(Owner_email=customer_email)
   

    if result_customer.exists() or result_owner.exists():
        Message = "This Email address already exist!!"
        return render(request,'register.html',{'Message':Message})
    else:
        customer=Customer(customer_firstname=customer_firstname,customer_lastname=customer_lastname,
        customer_dob=customer_dob,customer_gender=customer_gender,customer_mobileno=customer_mobileno,
        customer_email=customer_email,customer_password=customer_password,customer_address=customer_address,
        customer_city=customer_city,customer_state=customer_state,customer_country=customer_country,
        customer_pincode=customer_pincode)
        
        customer.save()
        request.session['user_email'] = customer_email
        isLogin = True
        return redirect('/Home/')

def Logout(request):
    global isLogout
    del request.session['user_email']
    isLogout = True
    Message = "Successfully Logged Out!!"
    return redirect('/')

def Home(request):
    if('user_email' not in request.session):
        return redirect('/signin/')
    customer_email = request.session.get('user_email')
    customer = Customer.objects.get(customer_email=customer_email)
    Clothes = Clothes.objects.all()
    Message="Welcome Aboard!!"
    return render(request,'Home.html',{'Clothes':Clothes,'Message':Message,'customer':customer})

def Profile(request):
    if('user_email' not in request.session):
        return redirect('/signin/')
    customer_email = request.session.get('user_email')
    customer = Customer.objects.get(customer_email=customer_email)
    return render(request,'Profile.html',{'customer':customer})

# def showdetails(request,Clothes_license_plate):
#     Clothes = Clothes.objects.get(Clothes_license_plate=Clothes_license_plate)
#     if('user_email' not in request.session):
#         return render(request,'showdetails_not_login.html',{'Clothes':Clothes})
#     else:
#         customer_email = request.session.get('user_email')
#         customer = Customer.objects.get(customer_email=customer_email)
#         return render(request,'showdetails_loggedin.html',{'Clothes':Clothes,'customer':customer})

# def CheckAvailability(request,Clothes_license_plate):
#     if('user_email' not in request.session):
#         return redirect('/signin/')

    RentClothes_Date_of_Booking=request.POST.get('RentClothes_Date_of_Booking','')
    RentClothes_Date_of_Return=request.POST.get('RentClothes_Date_of_Return','')
    
    RentClothes_Date_of_Booking = datetime.strptime(RentClothes_Date_of_Booking, '%Y-%m-%d').date()
    RentClothes_Date_of_Return = datetime.strptime(RentClothes_Date_of_Return, '%Y-%m-%d').date()

    rentClothes = RentClothes.objects.filter(Clothes_license_plate=Clothes_license_plate)
    Clothes = Clothes.objects.get(Clothes_license_plate=Clothes_license_plate)

    customer_email = request.session.get('user_email')
    customer = Customer.objects.get(customer_email=customer_email)

    if RentClothes_Date_of_Booking < date.today():
        Incorrect_dates = "Please give proper dates"
        return render(request,'showdetails_loggedin.html',{'Incorrect_dates':Incorrect_dates,'Clothes':Clothes,'customer':customer})

    if RentClothes_Date_of_Return < RentClothes_Date_of_Booking:
        Incorrect_dates = "Please give proper dates"
        return render(request,'showdetails_loggedin.html',{'Incorrect_dates':Incorrect_dates,'Clothes':Clothes,'customer':customer})
    
    days=(RentClothes_Date_of_Return-RentClothes_Date_of_Booking).days+1
    total=days*Clothes.Clothes_price
    
    rent_data = {"RentClothes_Date_of_Booking":RentClothes_Date_of_Booking, "RentClothes_Date_of_Return":RentClothes_Date_of_Return,"days":days, "total":total}
    
    for rv in rentClothes:

        if (rv.RentClothes_Date_of_Booking >= RentClothes_Date_of_Booking and RentClothes_Date_of_Return >= rv.RentClothes_Date_of_Booking) or (RentClothes_Date_of_Booking >= rv.RentClothes_Date_of_Booking and RentClothes_Date_of_Return <= rv.RentClothes_Date_of_Return) or (RentClothes_Date_of_Booking <= rv.RentClothes_Date_of_Return and RentClothes_Date_of_Return >= rv.RentClothes_Date_of_Return):
            if rv.isAvailable:
                Available = True
                Message = "Note that somebody has also requested for this Clothes from " + str(rv.RentClothes_Date_of_Booking) + " to " + str(rv.RentClothes_Date_of_Return)
                return render(request,'showdetails_loggedin.html',{'Message':Message,'Available':Available,'Clothes':Clothes,'customer':customer,'rent_data':rent_data})

            NotAvailable = True
            return render(request,'showdetails_loggedin.html',{'NotAvailable':NotAvailable,'dates':rv,'Clothes':Clothes,'customer':customer})

        # if (RentClothes_Date_of_Booking < rv.RentClothes_Date_of_Booking and RentClothes_Date_of_Return < rv.RentClothes_Date_of_Booking) or (RentClothes_Date_of_Booking > rv.RentClothes_Date_of_Return and RentClothes_Date_of_Return > rv.RentClothes_Date_of_Return):
        #     Available = True
        #     return render(request,'showdetails_loggedin.html',{'Available':Available,'Clothes':Clothes,'customer':customer,'rent_data':rent_data})


    Available = True
    return render(request,'showdetails_loggedin.html',{'Available':Available,'Clothes':Clothes,'customer':customer,'rent_data':rent_data})

def SentRequests(request):
    if('user_email' not in request.session):
        return redirect('/signin/')

    customer_email = request.session.get('user_email')
    customer = Customer.objects.get(customer_email=customer_email)

    rentClothes = RentClothes.objects.filter(customer_email=customer_email)
    if rentClothes.exists():
        Clothes = Clothes.objects.all()
        return render(request,'SentRequests.html',{'customer':customer,'rentClothes':rentClothes,'Clothes':Clothes})
    else:
        Message = "You haven't rented any Clothes yet!!"
        return render(request,'SentRequests.html',{'customer':customer,'rentClothes':rentClothes,'Message':Message})

def about_us(request):
    return HttpResponse('About Us')
    
def contact_us(request):
    return HttpResponse('Contact Us')

def search(request):
    return HttpResponse('search')