from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import Todo_form
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import datetime
from django.utils import timezone
from datetime import timedelta


# Create your views here.
def home(request):
    if request.method == 'GET':
        return render(request, 'todo/home.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/home.html',
                          {'form': AuthenticationForm(), 'error': 'Please verify your username and password'})
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


@login_required
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def your_todos(request):
    todos = Todo.objects.filter(user=request.user, completed_date__isnull=True)
    return render(request, 'todo/your_todos.html', {'todos': todos})


@login_required
def create_todo(request):
    if request.method == 'GET':
        return render(request, 'todo/create_todo.html', {'form': Todo_form()})
    else:
        try:
            form = Todo_form(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('your_todos')
        except ValueError:
            return render(request, 'todo/create_todo.html',
                          {'form': Todo_form(), 'error': 'The data is wrong, Try again'})


@login_required
def edit_todo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = Todo_form(instance=todo)
        return render(request, 'todo/edit_todo.html', {'todo': todo, 'form': form})
    else:
        try:
            form = Todo_form(request.POST, instance=todo)
            form.save()
            return redirect('your_todos')
        except ValueError:
            return render(request, 'todo/edit_todo.html', {'todo': todo, 'form': form, 'error': 'verify info'})


@login_required
def complete_todo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.completed_date = timezone.now()
        todo.save()
        return redirect('your_todos')


@login_required
def delete_todo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('your_todos')


@login_required
def completed(request):
    todos = Todo.objects.filter(user=request.user, completed_date__isnull=False).order_by('-completed_date')
    return render(request, 'todo/completed_todos.html', {'todos': todos})


@login_required
def all_todos(request):
    todos = Todo.objects.filter(user=request.user)
    return render(request, 'todo/all_todos.html', {'todos': todos})
