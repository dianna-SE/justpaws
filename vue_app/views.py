from genericpath import exists
import imghdr
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from .models import Profile, Post, FollowersCount
from django.contrib.auth.decorators import login_required

# Create your views here.

# INDEX #
@login_required(login_url='login')
def index(request):

    # adding a username and user profile image to allow dynamic changes to html #
    user_object = User.objects.get(username = request.user.username)
    user_profile = Profile.objects.get(user = user_object)

    # adding a post object to allow dynamic changes to html #
    posts = Post.objects.all()
    return render(request, 'index.html', {'user_profile': user_profile, 'posts': posts})

@login_required(login_url='login')
def upload(request):

    if request.method == 'POST' :
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user = user, image = image, caption = caption)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='login')
def settings(request):
    user_profile = Profile.objects.get(user = request.user)

    #
    if request.method == 'POST':

        # UPDATE USER BIO AND INFO - IF USER DOESN'T UPLOAD OR UPDATE ANYTHING
        if request.FILES.get('image') == None:
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.firstname = firstname
            user_profile.lastname = lastname
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        if request.FILES.get('image') != None:
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.firstname = firstname
            user_profile.lastname = lastname
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        return redirect('/')
    return render(request, 'settings.html', {'user_profile': user_profile})

# PROFILE #
@login_required(login_url='login')
def profile(request, pk):
    user_object = User.objects.get(username = pk)
    user_profile = Profile.objects.get(user = user_object)
    user_posts = Post.objects.filter(user = pk)
    user_post_length = len(user_posts)

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
    }

    return render(request, 'profile.html', context)

# FOLLOWS #
@login_required(login_url='login')
def follow(request):
    if request.method == "POST":
        follower = request.POST['follower']
        user = request.POST['user']

        # CHECK IF USER IS ALREADY FOLLOWING THE USER #
        if FollowersCount.objects.filter(follower = follower, user = user).first():
            delete_follower = FollowersCount.objects.get(follower = follower, user = user)
            delete_follower.delete()
            return redirect('/profile/' + user)
        else:
            new_follower = FollowersCount.objects.create(follower = follower, user = user)
            new_follower.save()
            return redirect('/profile/' + user)
    else:
        return redirect('/')

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



def message(request):
    return render(request, 'messages.html')