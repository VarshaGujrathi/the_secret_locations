# Create your views here.
from urllib import request
from django.shortcuts import render
from django.contrib import auth
import pyrebase
from images.views import home_img


Config = {
    'apiKey': "",
    'authDomain': "",
    'databaseURL': "",
    'projectId': "",
    'storageBucket': "",
    'messagingSenderId': "",
    'appId': "",
    'measurementId': ""
}
firebase = pyrebase.initialize_app(Config)
authe = firebase.auth()
database = firebase.database()
storage = firebase.storage()
def signin(request):    

    return render(request, "signIn.html")

def postsign(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        user = authe.sign_in_with_email_and_password(email, password)
        # print(user['idToken'])
    except:
        message="invalid credentials"
        return render(request, "signIn.html",{"message":message})
    
    name = database.child('users').child(user['localId']).child('details').child('name').get().val()
    print(name)
    session_id=user['idToken']
    request.session['uid']=str(session_id)
    
    # return render(request, "images.html", {"e":name})

    return home_img(request,user)
    

def logout(request):
    # auth.logout(request)
    try:
        del request.session['uid']
    except KeyError:
        pass
    
    return render(request, "home.html") 

def signup(request):
    return render(request, "signup.html")

def postsignup(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        user = authe.create_user_with_email_and_password(email,password)
    except:
        message = "Unable to create account"
        return render(request, "signup.html",{"message":message}) 
    uid= user['localId']
    data = {"name":name, "status":"1"}
    database.child("users").child(uid).child("details").set(data)
    
    #Email verification
    authe.send_email_verification(user['idToken'])
    return render(request, "signIn.html")

