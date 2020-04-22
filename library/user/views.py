from django.shortcuts import render,redirect
from system.models import Books,Faculty,Requests,issued
from datetime import datetime,date
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='/login/')
def Request(req):
    if req.method == "GET":
        temp=Requests.objects.filter(faculty_id=req.session['username'])
        l=[]
        totalissued = list(issued.objects.all().values_list('book_id',flat=True))
        print(totalissued)
        for t in temp:
          l.append(t.book_id.id)
        #print(l)  
        context={
            'books':Books.objects.all(),
            'myrequest': l,
            'totalissued': totalissued,
        }
        return render (req,'user/home.html',context=context)
    else:
        #print('POST request')
        #print(req.POST.get('status'))
        if req.POST.get('status') == "add":
            book=Books.objects.get(id=req.POST.get('bookid'))
            fac=Faculty.objects.get(id=req.session['username'])
            rqst=Requests(faculty_id=fac,book_id=book,date=datetime.now())
            rqst.save()
            return redirect('/library/Request/')
        else:
            print('request delete')
            book=Books.objects.get(id=req.POST.get('bookid'))
            fac=Faculty.objects.get(id=req.session['username'])
            rqst = Requests.objects.get(faculty_id=fac,book_id=book)
            print(rqst)
            rqst.delete()
            return redirect('/library/Request/')


@login_required(login_url='/login/')
def Allissued(request):
    totalissued = issued.objects.filter(faculty_id=request.session['username'])
    context={
        'totalissued':totalissued,
    }
    return render (request,'user/allissued.html',context=context)
    
@login_required(login_url='/login/')
def ChangePassword(request):
    if request.method == "GET":
        return render (request,'user/changepassword.html')
    if request.method == "POST":
        fac=Faculty.objects.get(id=request.session['username'])
        if fac.password == request.POST.get('oldpassword'):
            fac.password=request.POST.get('newpassword')
            fac.save()
            a=User.objects.get(username=request.session['username'])
            a.set_password(request.POST.get('newpassword'))
            a.save()
            return redirect('/library/Request/')
        else:
            r="Old Password Does Not Match"
            return render(request,'user/changepassword.html',{"error":r})

        


 

