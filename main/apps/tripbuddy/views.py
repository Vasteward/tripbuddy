from django.shortcuts import render, redirect, HttpResponse
from .models import *
import re
import bcrypt
from django.contrib import messages
from django.contrib.auth import logout
from django.conf import settings

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
def index(request):
    return render(request, 'tripbuddy/index.html')
#process
def register(request):
    #validations
    if request.method != "POST":
        return redirect('/')
    error = False
    if len(request.POST['first']) < 3:
        print('First name must be longer than 3 characters')
        messages.error(request, 'First name must be longer than 3 characters')
        error = True
    if len(request.POST['last']) < 3:
        print('Last name must be longer than 3 characters')
        messages.error(request, 'Last name must be longer than 3 characters')
        error = True
    if not request.POST['first'].isalpha() or not request.POST['last'].isalpha():
        print("First and Last name must only contain letters")
        messages.error(request, "First and Last name must only contain letters")
        error=True
    if not EMAIL_REGEX.match(request.POST['email']):
        print("Email is invalid")
        messages.error(request, "INVALID EMAIL!")
        error=True
    if request.POST['pw'] != request.POST['confirm_pw']:
        print("Passwords don't match")
        messages.error(request, "Passwords don't MATCH!")
        error=True
    if User.objects.filter(email = request.POST['email']):
        messages.info(request, "You're already apart of the fam. Proceed to login.")
        print("user is already in the database")
        return redirect('/')
        error=True
    if error:
        print("WE HAVE ERRORS")
        return redirect('/')
    else: 
        hashed = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt())
        #if good, hash pw
        #store in db
        #generate error msgs
        newUser = User.objects.create(first_name = request.POST['first'], last_name=request.POST['last'], email=request.POST['email'], password=hashed)
        request.session['user_id'] = newUser.id
        print("SUCCESS")
        messages.success(request, 'SUCCESS')
        request.session['greeting'] = "Glad you signed up!"
        return redirect('/success')

def validate_login(request):
    User.objects.all().values()
    if request.method != "POST":
        return redirect('/')
    #validations
    #check if user is in db
    #generate error msgs
    user = User.objects.filter(email=request.POST['email'])

    if len(user) > 0:
        print("THERE'S SOMETHING HERE")
        #if the email is in the db, decrypt the password and check if it is the same as what is stored
        if bcrypt.checkpw(request.POST['pw'].encode(), user[0].password.encode()):
            print('password match')
            #put the person in session, the user[0] is the first person in the list, grabbing the id and put it in session 
            request.session['user_id'] = user[0].id
            request.session['greeting'] = "Welcome "
            #redirect to the success page
            return redirect('/success')
        else: 
            #flash, password doesn't match
            print(user[0].password.encode())
            print("password does not match")
            messages.error(request, "Password does not match")
            return redirect('/')
    else:
        # redirect to registration and send message
        print("The person is a newb.")
        messages.error(request, "Welcome new user. Please, register.")
        print("BATMAN"*20)
    return redirect('/success')

def success(request):
    # Fetch records from db
    # create a dictionary to pass to the browser

    if not 'user_id' in request.session:
        return redirect('/')
    context = {
        # query the db to get the user_id of the person that is in session 
        "the_user": User.objects.get(id=request.session['user_id']),
        "greeting": request.session['greeting'],
        "users" : User.objects.all(),
        "trip": Trip.objects.all()
    }
    return render(request, 'tripbuddy/dashboard.html', context)

def create_page(request):
    if not 'user_id' in request.session:
        return redirect('/')

    context = {
        # "trips_of_individual": User.objects.get(id=id).all_trips.values(), 
        "user": User.objects.get(id=request.session['user_id']),
        "admin": User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'tripbuddy/create.html')

def create_trip(request):
    if request.method != "POST":
        return redirect('/')
    if not 'user_id' in request.session:
        return redirect('/')
    context = {
        # "trips_of_individual": User.objects.get(id=id).all_trips.values(), 
        "user": User.objects.get(id=rqeuest.session['user_id']),
        "admin": User.objects.get(id=id)
    }
    error = False
    if len(request.POST['destination']) < 3:
        print('Destination name is too short')
        messages.error(request, 'Author must be longer than 3 characters')
        error = True
    if len(request.POST['description']) < 10:
        print('Not excited enough')
        messages.error(request, 'Description must be longer than 10 characters')
        error = True

    if error:
        return redirect('/create')
    else: 
        explorer = User.objects.get(id=request.session['user_id'])
        explorer.save()
        expedition=request.POST['destination'], description=request.POST['description']
        expedition.save()
        explorer.all_trips.add(expedition)
        explorer.save()

        # Trip.objects.create(destination=request.POST['destination'], description=request.POST['description'], user = User.objects.get(id=request.session['user_id']))

    print("\n\n")
    print("\n\n")
    print("SUPERWOMAN"*20)
    return redirect('/show')


def show(request, id):
    context = {
        "trips_of_individual": User.objects.get(id=id).all_trips.values(), 
        "user": User.objects.get(id=id),
        "admin": User.objects.get(id=id)
    }
    return render(request,'tripbuddy/show.html', context) 