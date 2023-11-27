from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from home.models import *
from home.forms import *


# Create your views here.

def index(request):
    return render(request, 'index.html')



def SignUp(request):
    if request.method == 'POST':
        user_form=UserCreateForm(request.POST)
        profile=profile_form(request.POST,request.FILES)
        if user_form.is_valid() and profile.is_valid():
            user=user_form.save()
            pro=profile.save(commit=False)
            pro.user=user
            pro.save()
            return redirect(reverse_lazy("home:login"))
    return render(request, 'signup.html',{'Userform':UserCreateForm,'profile_form':profile_form})

@login_required
def dashboard(request):
    user=request.user
    profile_data=profile.objects.filter(user=user.id).all()
    print(profile_data)
    return render(request, 'dashboard.html',{'user':user, 'profile':profile_data})