from django.shortcuts import render

# Create your views here.


def signup_user(request):
    return render(request, 'todo/signup_user.html')
