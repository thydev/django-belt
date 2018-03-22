from django.shortcuts import render, redirect
from django.contrib import messages
from models import User
import bcrypt
from datetime import datetime

# Create your views here.
def index(request):
    request.session.modified = True
    if 'loggedin' not in request.session:
        request.session['loggedin'] = {
            'id': -1,
            'name': "undefined"
        }
    return render(request, 'login/index.html')

def login(request):
    request.session.modified = True
    if request.method != "POST":
        return redirect('/')
    email = request.POST['email']
    user = User.objects.filter(email = email)
    
    if len(user) == 0:
        messages.error(request, "This email {} does not exist in the system".format(email), extra_tags="login")
        # messages.add_message(request,messages.WARNING)
    else:
        password = request.POST['password']
        # To check if a password encrypted in bcrypt matches another
        user = user.first()
        if not bcrypt.checkpw(password.encode(), user.password.encode()):
            messages.error(request, "Incorrect password.", extra_tags="login")
            return redirect('/')
        messages.success(request, "Successfully logged in !, Welcome {} {}".format(user.first_name, user.last_name))
        request.session['loggedin'] = {
            'id': user.id,
            'name': "{} {}".format(user.first_name, user.last_name)
        }
        # return redirect('/login/success')
        return redirect('/books')

    return redirect('/')

def create(request):
    request.session.modified = True
    if request.method != "POST":
        return redirect('/')
    
    print "date===>", request.POST['date_birth']
    print "dj date===>", datetime.now().strftime("%Y-%m-%d")
    if  request.POST['date_birth']:
        print request.POST['date_birth'] < datetime.now().strftime("%Y-%m-%d")
        
    return redirect('/')

    # Validation for creating new object
    errors = User.objects.create_validator(request.POST)
    if len(errors) > 0:
        for tag, error in errors.iteritems():
            # messages.error(request, error, extra_tags=tag)
            messages.error(request, error, extra_tags="create")
        return redirect('/')

    password = request.POST['password']
    # Encript the password by using bscrypt
    password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = password)
    messages.success(request, "Successfully logged in!")
    request.session['loggedin'] = {
        'id': user.id,
        'name': "{} {}".format(user.first_name, user.last_name)
    }
    # return redirect('/login/success')
    return redirect('/books')

def success(request):
    # Redirect to the login if the user did not log in yet
    if request.session['loggedin']['id'] == -1:
        return redirect('/')

    # Display success message
    return render(request, 'login/success.html')

def logout(request):
    request.session.modified = True
    request.session['loggedin'] = {
            'id': -1,
            'name': "undefined"
        }
    return redirect('/')

def showuser(request, id):
    # In books app or in login app?
    pass