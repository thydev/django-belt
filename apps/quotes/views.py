from django.shortcuts import render, redirect
from django.contrib import messages
from models import Quote, Favorite
from ..login.models import User

def isLogin(request):
    if 'loggedin' not in request.session:
        request.session['loggedin'] = {
            'id': -1,
            'name': "undefined"
        }
    # Redirect to the login if the user did not log in yet
    if request.session['loggedin']['id'] != -1:
        return True
    return False


# Display all quote, favorite quotes, add new quote
def index(request):
    if not isLogin(request):
        return redirect('/')
    
    user = User.objects.get(id=request.session['loggedin']['id'])
    favorites = Favorite.objects.filter(user=user)

    object_id_list = []
    #built object id lsit to exclude from quotes
    for fav in user.user_favorites.all():
        object_id_list.append(fav.quote.id)

    quotes = Quote.objects.all().exclude(id__in = object_id_list).order_by('-created_at')

    print favorites
    print user.user_favorites.all().values('quote')

    context = {
        'quotes': quotes,
        'favorites': favorites
    }
    return render(request, 'quotes/index.html', context)

#Create a new quote
def create(request):

    if not isLogin(request):
            return redirect('/')

    if request.method != "POST":
        return redirect('/quotes')

    #Create quote 
    errors = Quote.objects.create_validator(request.POST)
    if len(errors) > 0:
        for tag, error in errors.iteritems():
            # messages.error(request, error, extra_tags=tag)
            messages.error(request, error, extra_tags="create")
        return redirect('/quotes')

    user = User.objects.get(id=request.session['loggedin']['id'])
    quote = Quote.objects.create(
        poster = user, 
        quoted_by = request.POST['quoted_by'],
        message = request.POST['message']
    )

    return redirect('/quotes')

# Add favorite quote
def add_favorite(request, quote_id):
    print "add favorite"

    if not isLogin(request):
            return redirect('/')
            
    if request.method != "POST":
        return redirect('/quotes')

    user = User.objects.get(id=request.session['loggedin']['id'])
    quote = Quote.objects.get(id=quote_id)
    Favorite.objects.create(
        user = user,
        quote = quote
    )
    return redirect('/quotes')

def delete_favorite(request, fav_id):
    print "delete favorite"

    if not isLogin(request):
            return redirect('/')
            
    if request.method != "POST":
        return redirect('/quotes')

    #Delete from favorite list
    Favorite.objects.get(id=fav_id).delete()

    return redirect('/quotes')

def showuser(request, id):

    print "show suser"
    if not isLogin(request):
            return redirect('/')

    context = {
        'user': User.objects.get(id=id),
    }
    return render(request, 'quotes/showuser.html', context)