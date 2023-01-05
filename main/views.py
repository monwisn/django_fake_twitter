from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse

from main.models import Profile


def home(request):
    return render(request, 'main/home.html')
    # return HttpResponse('Hello world')


def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'main/profile_list.html', {'profiles': profiles})
    else:
        messages.success(request, 'You Must Be Logged In To View This Page...')
        return redirect('main:home')
