from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.template.context_processors import csrf
from django.views.generic import TemplateView
from django.db import IntegrityError
import traceback
from django.contrib.auth.decorators import login_required
from django.conf import settings

# Create your views here.
def mylogin(request):
    #print(settings.Faculty_DueCharge)
    #print(request.user.is_anonymous)
    if(request.user.is_anonymous):
        return render(request,'login/index.html')
    return HttpResponseRedirect("/library/Request/")

def authenticate(request):
    try:
        username=request.POST.get('username','')
        password=request.POST.get('password','')
        a=User.objects.get(username=username)
        print(a)
        x=auth.authenticate(username=username,password=password)
        print(x)
        if x is not None:
            auth.login(request,x)
            request.session['username']=username
            if username == "admin":
                return HttpResponseRedirect("/administrator/Books/")
            else:
                return HttpResponseRedirect("/library/Request/")
        else:
             r="Invalid Username or Password"
             return render(request,'login/index.html',{"error":r})
    except:
        r="Invalid Username or Password"
        return render(request,'login/index.html',{"error":r})

def logout(request):
    auth.logout(request)
    request.session['username']=None
    return HttpResponseRedirect('/login/')

def createadmin(request):
    a=User.objects.create_user("admin","admin@gmail.com","admin")
    a.save()
    return HttpResponse("added")
