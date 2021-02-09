import plaid
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from plaid_config import PlaidConfig
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from .models import PlaidKey

from .forms import RegisterForm

conf = PlaidConfig()

client = plaid.Client(client_id=conf.PLAID_CLIENT_ID,
                      secret=conf.PLAID_SECRET,
                      environment=conf.PLAID_ENV)


def register_app(request):
    print("IN REGISTER_APP")
    if request.method != 'POST': print("NOT A POST REQUEST")
    username = request.POST['username']
    password = request.POST['password']
    conf_password = request.POST['conf_password']
    email = request.POST['email']

    if User.objects.filter(username=username).exists():
        print("FAILED: Username already exists")
    
    elif password!=conf_password:
        print("FAILED: Passwords do not match")
    
    else:
        user = User.objects.create_user(username, email, password)
        login(request, user)
        print("SUCCESS: Logged in", username)

    



def register(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            conf_password = form.cleaned_data['conf_password']
            email = form.cleaned_data['email']

            # process the data in form.cleaned_data as required
            if User.objects.filter(username=username).exists():
                form = RegisterForm()
                return render(request, 'register/register.html', {'form': form, 'user_err': True, 'pass_err': False})
            
            elif password!=conf_password:
                form = RegisterForm()
                return render(request, 'register/register.html', {'form': form, 'user_err': False, 'pass_err': True})
            
            else:
                user = User.objects.create_user(username, email, password)
                login(request, user)
                
                #redirect to plaid
                return HttpResponseRedirect(reverse('register:link_plaid'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegisterForm()

    return render(request, 'register/register.html', {'form': form, 'user_err': False, 'pass_err': False})

def get_link_token(request):
    print("enter get link")
    
    # Create a link_token for the given user
    response = client.LinkToken.create({
      'user': {
        'client_user_id': request.user.username,
      },
      'products': conf.PLAID_PRODUCTS,
      'client_name': 'My App',
      'country_codes': conf.PLAID_COUNTRY_CODES,
      'language': 'en',
    })

    link_token = response['link_token']

    print("link_token", link_token)
    
    # Send the data to the client
    return JsonResponse(response)

def link_plaid(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/accounts/login/')
        
    return render(request, 'register/link.html', {})
    
def get_access_token(request):
    print("IN GET ACCESS TOKEN")
    public_token = request.POST['public_token']
    exchange_response = client.Item.public_token.exchange(public_token)

    key = PlaidKey(user=request.user, access_token=exchange_response['access_token'], item_id=exchange_response['item_id'])
    key.save()

    print('access token: ' + exchange_response['access_token'])
    print('item ID: ' + exchange_response['item_id'])


