from django.urls import path,include
from django.conf.urls import url

from user import views

urlpatterns = [
    #path('', views.index, name='index'),
    url(r'^Request/$', views.Request),
    url(r'^MyBooks/$', views.Allissued),
    url(r'^ChangePassword/$', views.ChangePassword),
]