from genericpath import exists
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from .models import Profile
from django.contrib.auth.decorators import login_required

# Create your views here.

# INDEX #
@login_required(login_url='login')
def index(request):
    return render(request, 'index.html')

@login_required(login_url='login')
def settings(request):
    return render(request, 'settings.html')

# PROFILE #
def profile(request):
    return render(request, 'profile.html')




# LOGIN #
def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # AUTHENTICATE USERNAME AND PASSWORD #
        user = auth.authenticate(username = username, password = password)

        # IF USER IS INCLUDED IN DATABASE #
        if user is not None:
            auth.login(request, user)
            return redirect('/')

        # IF USER INFO IS INCORRECT #
        else:
            messages.info(request, 'invalid username or password.')
            return redirect('login')

    else:
        return render(request, 'login.html')




# LOGOUT #
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')
# LOGOUT #






# REGISTER #
def register(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']


        if password == confirmpassword:

            # IF EMAIL HAS ALREADY BEEN REGISTERED #
            if User.objects.filter(email = email).exists():
                messages.info(request, 'this email is already taken.')
                return redirect('register')

            # IF USERNAME HAS ALREADY BEEN REGISTERED #
            elif User.objects.filter(username = username).exists():
                messages.info(request, 'this username is already taken.')
                return redirect('register')
            
            # ELSE, CREATE A NEW USERNAME, EMAIL, PASSWORD #
            else:
                user = User.objects.create_user(
                    username = username, 
                    email = email, 
                    password = password
                )
                user.save()

                # LOG USER IN AND DIRECT TO REDIRECT TO PERSONALIZED SETTINGS #
                user_login = auth.authenticate(
                    username = username, 
                    password = password
                )
                auth.login(request, user_login)


                # CREATE PROFILE OBJECT FOR NEW USER #
                user_model = User.objects.get(username = username)
                new_profile = Profile.objects.create(user = user_model, id_user = user_model.id)

                new_profile.save()
                return redirect('settings')


        # IF PASSWORD DOES NOT MATCH WITH CONFIRM PASSWORD #
        else: 
            messages.info(request, 'password does not match.')
            return redirect('register')


    else:
        return render(request, 'register.html')