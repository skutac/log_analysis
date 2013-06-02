from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

def create_user(request):
    user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    user.last_name = 'Lennon'
    user.save()
    return render_to_response("", {})

def get_user(username):
    user = User.objects.get(username=username)
    return user

def login_user(request):
    print request
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect("index")
    else:
        return HttpResponseRedirect("log_analysis/index")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect("login")