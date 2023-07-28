from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from random import randint
from django.contrib.auth import get_user_model,logout,authenticate
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login
from datetime import datetime
import pytz

#variables
User=get_user_model()
set_time_zone=pytz.timezone('Asia/Kolkata')

#Useful Functions
def fetch_accounts_data(username,req_email=False,otp_needed=False,req_pass=False,is_verified=False):
    '''Fetch data from database'''
    #Checks user exist or not!
    try:
        try:
            accounts=User.objects.get(username=username)
        except:
            username=BaseUserManager.normalize_email(username)
            accounts=User.objects.get(email=username)
        account_data={'username_exist':True}
        if req_email==True:
            account_data['email']=accounts.email
        if otp_needed==True:
            account_data['otp']=(accounts.otp,accounts.otp_date)
        if req_pass:
            account_data['password']=accounts.password
        if is_verified:
            account_data['is_verified']=accounts.authenticate_email
        return account_data
    
    except Exception as e:
        if "not exist" in str(e):
            print(e)
            return {'username_exist':False}
        print('I am Fetch account',e)
def send_email_to_client(client_mail=None,message=None,username=None,subject=None):
    '''Send mail to user'''
    if username !=None:
        client_mail=fetch_accounts_data(username,req_email=True)['email']
    from_email=settings.EMAIL_HOST_USER
    recipient_list=[client_mail]
    return send_mail(subject, message,from_email,recipient_list)
def provide_otp(username):
    '''This will provide OTP and check it is valid or not!'''
    current_date=datetime.now(set_time_zone)
    otp,otp_gen_date=fetch_accounts_data(username,req_email=True,otp_needed=True)['otp']
    try:
        duration=((current_date-otp_gen_date).total_seconds())//60
        if duration >10:
            return False,None
        else:
            return True,otp
    except:
        return None,None,None

# Create your views here.
def handlelogin(request):
    '''This will handle login'''
    parms={}
    if request.method=='POST':
        get_data=request.POST
        username=get_data['username']
        password=get_data['password']
        if fetch_accounts_data(username=username)['username_exist'] ==False:
            parms['is_error'],parms['error_mssg']=True,'Username or Email doesnot exist!'
            return render(request,'accounts/login.html',parms)
        if check_password(password,fetch_accounts_data(username=username,req_pass=True)['password'])==False:
            parms['is_error'],parms['error_mssg'],parms['username']=True,'Wrong Password!',username
            return render(request,'accounts/login.html',parms)
        if fetch_accounts_data(username=username,is_verified=True)['is_verified'] == False:
            parms['is_error'],parms['error_mssg'],parms['username'],parms['is_verified']=True,'Email not verified! Verify First.',username,True
            return render(request,'accounts/login.html',parms)
        #Username Exist and password is correct user is verified
        user=authenticate(username=username,password=password)
        if user == None:
            username=fetch_accounts_data(username=username,req_email=True)['email']
            print(username)
            user=authenticate(username=username,password=password)
        login(request,user)
        return redirect('/')
    return render(request,'accounts/login.html',parms)
def handlelogout(request):
    '''This will handle logout'''
    logout(request)
    return redirect('/accounts/login')
def signup(request):
    '''This will handle signup'''
    parms={'load_signup':True,'load_otp':False,'load_name':False}
    if request.method == "POST":
        user_entered=request.POST
        what_to_load=user_entered['what_to_load']
        parms={'load_signup':int(what_to_load[0]),'load_otp':int(what_to_load[1]),'load_name':int(what_to_load[2])}
        #loads signup page
        if parms['load_signup']==True:
            email=user_entered['email']
            username=user_entered['username']
            password=user_entered['pass1']
            confirm_password=user_entered['pass2']
            #checks
            #Checks username exist in database or not
            username_exist=fetch_accounts_data(username)
            if username_exist['username_exist']==True:
                parms['is_error'],parms['error_message']=True,"Username already taken!"
                return render(request,'accounts/signup.html',parms)
            #checks confirm password
            if password!=confirm_password:
                parms['username'],parms['email']=username,email
                parms['is_error'],parms['error_message']=True,"Password doesn't match!"
                return render(request,'accounts/signup.html',parms)
            #checks email is valid
            try:
                otp=str(randint(1000,9999))
                message=f'Welcome {username} you have successfully created your memer account.Please verify your account \n OTP: {otp} \n Valid only for 10 minutes '    
                myuser=User.objects.create_user(email,password)
                send_email_to_client(email,message,subject='OTP Verification | MEMER')
                myuser.username=username
                myuser.otp=otp
                myuser.otp_date=datetime.now(set_time_zone)
                myuser.save()
                parms['load_otp'],parms['load_signup'],parms['username'],parms['is_success'],parms['success_message'],parms['success_message1']=True,False,username,True,f'OTP send to {email}.','Valid only for 10 minutes'
            except Exception as e:
                parms['username']=username
                if "UNIQUE constraint failed" in str(e):
                    parms['is_error'],parms['error_message']=True,"Email Already Registered!"
                else:
                    parms['is_error'],parms['error_message']=True,"Invalid Email"
                
        #loads OTP page
        elif parms['load_otp']==True:
            user_entered=request.POST
            username=user_entered['username']
            parms['username']=username
            otp_entered=user_entered['otp1']+user_entered['otp2']+user_entered['otp3']+user_entered['otp4']
            otp_status,otp=provide_otp(username)
            if otp_status:
                if otp_entered!=otp:
                    parms['is_error'],parms['error_message']=True,"Wrong OTP!"
                    return render(request,'accounts/signup.html',parms)
                else:
                    parms['load_otp'],parms['load_name']=False,True
                    #Push to database email verified
                    myuser=User.objects.get(username=username)
                    myuser.authenticate_email=True
                    myuser.save()
                    message=f'Hello {username}, you have successfully verified your account. Welcome to memers family!'
                    subject='Welcome to MEMERS family.'
                    send_email_to_client(username=username,message=message,subject=subject)
                    return render(request,'accounts/signup.html',parms)
            else:
                re_gen=bool(user_entered['re_gen'])
                if re_gen:
                    otp=str(randint(1000,9999))
                    message=f'Welcome {username}, Your OTP is generated.Please verify your account \n OTP: {otp} \n Valid only for 10 minutes '    
                    send_email_to_client(username=username,message=message,subject='OTP Verification | MEMER')
                    myuser=User.objects.get(username=username)
                    myuser.otp=otp
                    myuser.otp_date=datetime.now(set_time_zone)
                    myuser.save()
                    parms['is_success'],parms['success_message'],parms['expired']=True,"OTP expired. New one sent.",False
                else:
                    parms['is_error'],parms['error_message'],parms['expired']=True,"OTP expired!",True
                    return render(request,'accounts/signup.html',parms)
        
        #loads name page
        elif parms['load_name']==True:
            username=user_entered['username']
            parms['username']=username
            fname,lname,dob=user_entered['fname'],user_entered['lname'],user_entered['dob']
            myuser=User.objects.get(username=username)
            myuser.first_name=str(fname).capitalize()
            myuser.last_name=str(lname).capitalize()
            myuser.dob=dob
            myuser.save()
            return redirect('/accounts/login')
    return render(request,'accounts/signup.html',parms)
def forgot_password(request):
    '''This will handle forgot_password'''
    parms={}
    return render(request,'accounts/forgotpassword.html',parms)