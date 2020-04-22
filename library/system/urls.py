from django.urls import path,include
from django.conf.urls import url

from system import views

urlpatterns = [
    #path('', views.index, name='index'),
    url(r'^Books/$', views.AllBooks),
    url(r'^NewMember/$', views.Add),
    url(r'^Faculties/$', views.AllFaculty),
    url(r'^Editdata/$', views.Editdata),
    url(r'^Delete/$', views.DeleteFac),
    url(r'^CSV/$', views.InputCSV),
    url(r'^ChangebookStatus/$', views.ChangebookStatus),
    url(r'^base_layout/$', views.BaseLayout),
    url(r'^BookRequest/$', views.BookRequests),
    url(r'^BookIssued/$', views.BookIssued),
    url(r'^Email/$', views.Notify),
    url(r'^OverDue/$', views.OverDue),
    url(r'^Send_Notification/$', views.Send_Notification),
    url(r'^ChangeSettings/$', views.ChangeSetting),
    url(r'^aboutus/$', views.AboutUs),
    url(r'^AddBook/$', views.AddBook),
]