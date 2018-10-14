from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                User.objects.get(username=request.POST['username'])
                return render(request, 'signup.html', {'error': 'Username has already been taken.'})
            except User.DoesNotExist:
                User.objects.create_user(username=request.POST['username'], password=request.POST['password1'], is_active=False)
                return render(request, 'post_signup.html')
        else:
            return render(request, 'signup.html', {'error': 'Passwords do not match.'})
    else:
        return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('pedigree')
        else:
            return render(request, 'login.html', {'error': 'Username or Password does not exist.'})
    else:
        return render(request, 'login.html')


def logout(request):
    # TO DO neet to go to homepage and logout
    # if request.method == 'POST':
    auth.logout(request)
    return redirect('home')