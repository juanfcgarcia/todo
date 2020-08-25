from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate


# Create your views here.
def home(request):
    if request.method == 'GET':
        return render(request, 'todo/home.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/home.html', {'form': AuthenticationForm(), 'error': 'Please verify your username and password'})
        else:
            login(request, user)
            return redirect('your_todos')

def signup_user(request):
    if request.method == 'GET':
        return render(request, 'todo/signup_user.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('your_todos')
            except IntegrityError:
                return render(request, 'todo/signup_user.html',
                              {'form': UserCreationForm(), 'error': 'That username has already been taken'})

        else:
            return render(request, 'todo/signup_user.html',
                          {'form': UserCreationForm(), 'error': 'Passwords are not same'})


def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def your_todos(request):
    return render(request, 'todo/your_todos.html')
