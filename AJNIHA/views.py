from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib.auth.forms import UserCreationForm
#from .models import Contact, Blog, Course
# Create your views here.
#from django.http import HttpResponse
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


#string-->http response
@login_required(login_url='loginPage')
def index(request):
    return render(request,['AJNIHA/index.html'])

def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form=CreateUserForm()
        if request.method=='POST':
            form=CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,'Account was created for '+form.cleaned_data.get('username'))
                return redirect('loginPage')
        context={'form':form}
        return render(request,'AJNIHA/register.html',context)




def loginPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method=='POST':
            #taking thr value of these fields
            username=request.POST.get('username')
            password=request.POST.get('password')
            print(username+" "+password)
            user =authenticate(request,username=username,password=password)
            print(user)
            if user is not None:
                login(request,user)
                return redirect('index')
            else:
                messages.info(request,'username or password is incorrect')

        context={}
        return render(request,['AJNIHA/login.html'],context)

def logoutUser(request):
    logout(request)
    return redirect('loginPage')