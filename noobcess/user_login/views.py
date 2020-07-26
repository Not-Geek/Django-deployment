from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from .forms import UserForm


def index(request):
    return render(request,'user_login/index.html',)

def register(request):
    registered = False

    if request.method=="POST":
        form = UserForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            registered =True
        else:
            print(form.errors)
    else:
        form = UserForm()
    return render(request,'user_login/register.html',{ 'form':form,
                                                        'registered': registered})

@login_required
def profile(request):
    return render(request,'user_login/profile.html')


def login_user(request):

    if request.method == "POST":

         username = request.POST.get('username')
         password = request.POST.get('password')
         user = authenticate(username =username, password = password)
         if user:
             if user.is_active:
                 login(request,user)
                 return render(request,'user_login/profile.html', {'username':username})
             else:
                return HttpResponse("Account not active")
         else:
            return HttpResponse("Invalid username and Password")
    return render(request,'user_login/login.html')

@login_required
def logout_user(request):
    logout(request)
    return redirect('/')
