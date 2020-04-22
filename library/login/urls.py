from django.urls import path
from django.conf.urls import url,include
from login.views import mylogin,authenticate,logout,createadmin
from django.contrib.auth.views import LoginView
urlpatterns = [ 
    path('',mylogin, name='index'),
    path('authenticate/',authenticate, name='auth'),
    path('logout/',logout, name='logout'),
    path('addadmin/',createadmin, name='createadmin'),
    ]