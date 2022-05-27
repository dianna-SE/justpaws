from genericpath import exists
import imghdr
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from .models import Profile, Post, FollowersCount, PostUser
from django.contrib.auth.decorators import login_required
from itertools import chain
import random

# Create your views here.

# INDEX #
@login_required(login_url='login')
def index(request):

    # adding a username and user profile image to allow dynamic changes to html #
    user_object = User.objects.get(username = request.user.username)
    user_profile = Profile.objects.get(user = user_object)


    # contains the user's and followers' feeds
    user_following_list = []
    feed = []

    user_following = FollowersCount.objects.filter(follower = request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    # append to the feed list
    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user = usernames)
        feed.append(feed_lists)

    # import chain to be able to convert feed to a list
    feed_list = list(chain(*feed))

    # USER SUGGESTIONS #
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username = user.user)
        user_following_all.append(user_list)
    
    # GRABS ALL THE USERS THAT THE USER IS NOT FOLLOWING INTO A LIST TO SUGGEST
    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username = request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
    # RANDOMIZE SUGGESTED AND SHOW ONLY 4 FROM THE LIST #
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)
    
    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user = ids)
        username_profile_list.append(profile_lists)
    
    suggestions_username_profile_list = list(chain(*username_profile_list))

    return render(request, 'index.html', {'user_profile': user_profile, 'posts': feed_list, 'suggestions_username_profile_list': suggestions_username_profile_list[:4]})




@login_required(login_url='login')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        file_name = request.POST['filename']
        course_name = request.POST['coursename']

        new_post = Post.objects.create(user = user, image = image, caption = caption, file_name = file_name, coursename = course_name)
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

    follower = request.user.username
    user = pk

    # CHECK INSIDE DATABASE IF USER IS ALREADY FOLLOWED
    if FollowersCount.objects.filter(follower = follower, user = user).first():
        button_text = 'unfollow'
    else:
        button_text = 'follow'

        # GETTING USER'S FOLLOWER COUNT AND FILTERING ONLY THE USER'S FOLLOWERS
    user_followers = len(FollowersCount.objects.filter(user = pk))
    user_following = len(FollowersCount.objects.filter(follower = pk))


    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
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







# SEARCH #
@login_required(login_url='login')
def search(request):
    # GET USER PROFILE IMAGE !!IMPORTANT TO UTILIZE!!#
    user_object = User.objects.get(username = request.user.username)
    user_profile = Profile.objects.get(user = user_object)

    if request.method == 'POST':
        username = request.POST['username']
        # GETS LIST OF ALL THE OBJECTS CONTAINED IN THE USERNAME AND SEARCHES THE DATABASE #
        username_object = User.objects.filter(username__icontains = username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user = ids)
            username_profile_list.append(profile_lists)

        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})







@login_required(login_url='login')
def message(request):
    return render(request, 'messages.html')