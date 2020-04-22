from django.shortcuts import render,redirect
from django.template.context_processors import csrf
from django.template import loader
from django.http import HttpResponse
from django.http import JsonResponse

from django.template.context_processors import csrf
from system.models import issued,Books,Faculty,Requests,issued,StudentIssued
from datetime import datetime,date

from django.core import mail
from django.core.mail import EmailMessage,send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.files import File

# Create your views here.

def BaseLayout(request):
    return render(request,'administrator/base.html')

@login_required(login_url='/login/')
def AllFaculty(request):
    all_faculty=Faculty.objects.all()
    req_count = Requests.objects.all()
    print(req_count)
    t = datetime(date.today().year, date.today().month, date.today().day, 0, 0)
    mydate=t.strftime('%Y-%m-%d')
    allissued = issued.objects.filter(return_date__lt=mydate)
    context={
        'faculties':all_faculty,
        'req_count':req_count,
        'overdue':allissued
    }
    return render(request,'administrator/Member.html',context=context)

@login_required(login_url='/login/')
def AllBooks(request):
    req_count = Requests.objects.all()
    all_books= Books.objects.all()
    #print(all_books)
    t = datetime(date.today().year, date.today().month, date.today().day, 0, 0)
    mydate=t.strftime('%Y-%m-%d')
    allissued = issued.objects.filter(return_date__lt=mydate)
    context={
        'books':all_books,
        'req_count':req_count,
        'overdue':allissued
    }
    return render(request,'administrator/books.html',context=context)
    #return render_to_response('administrator/books.html', context=context)


@login_required(login_url='/login/')
def Add(request):
    if request.method == "POST":
        id = request.POST.get('id','')
        name= request.POST.get('name','')
        email= request.POST.get('email','')
        phone_no = request.POST.get('phone_no','')
        if request.POST.get('ea','') == "Add":
            print(phone_no)
            password= User.objects.make_random_password(length=8) #Generate password randomly
            print(password) #Print Randomly generated password 
            a=User.objects.create_user(id,email,password)
            a.save()
            faculty= Faculty(id=id,name=name,email=email,phone_no=phone_no,password=password,date_joined=datetime.now())
            faculty.save()
            # Receiver email
            to=email
            # body and subject of mail 
            body="Hey %s ! \n \n Password for your Ce-Department Library account is %s \n"%(name,password)
            #Composing email and  sending mail
            email=EmailMessage('CE-Department',body,to=[to])
            email.send()
        else:
            faculty = Faculty.objects.get(id=id)
            faculty.name = name
            faculty.email = email
            faculty.phone_no = phone_no
            faculty.save()
        all_faculty=Faculty.objects.all()
        return redirect('/administrator/Faculties/')

@login_required(login_url='/login/')
def AddBook(request):
    if request.method == "POST":
        last_book = Books.objects.last()
        #print(last_book.id)
        last_id = last_book.id.split('-')
        #print(last_id)
        id = int(last_id[1]) + 1
        Title = request.POST.get('Title','')
        id= "CE-"  + str(id)
        Publisher= request.POST.get('Publisher','')
        Author= request.POST.get('Author','')
        a=Books(sr_no=int(last_book.sr_no)+1,id=id,title=Title,publisher=Publisher,author=Author,available=True)
        a.save()
    return redirect('/administrator/Books/')



@login_required(login_url='/login/')
def Editdata(request):
    if request.method == "GET":
        #print(request.GET.get('id'))
        fac_data = Faculty.objects.get(id=request.GET.get('id'))
        #print(fac_data.id)
        data={
            'id':fac_data.id,
            'name':fac_data.name,
            'email':fac_data.email,
            'phone_no':fac_data.phone_no,
        }
        return JsonResponse(data)

@login_required(login_url='/login/')
def DeleteFac(request):
    if request.method == "GET":
        fac_data = Faculty.objects.get(id=request.GET.get('id'))
        fac_data.delete()
        data={
            'cond':True
        }
        return JsonResponse(data)

@login_required(login_url='/login/')   
def InputCSV(request):
    if request.method == "POST":
        if(request.POST.get('type') == "fac"):
            csv_file = request.FILES["csv_file"]
            file_data = csv_file.read().decode("utf-8")	
            lines = file_data.split("\n")
            for line in lines:			
                fields = line.split(',')
                print(fields)
                faculty= Faculty(id=fields[0],name=fields[1],email=fields[2],phone_no=fields[3],password=fields[4],date_joined=datetime.now())
                faculty.save()
                print(line)
            return redirect('/administrator/Faculties/')
        elif(request.POST.get('type') == "Book"):
            return redirect('/administrator/Faculties/')
        else:
            return redirect('/administrator/Faculties/')
    else:
        return render(request,'administrator/upload.html')

"""def UploadDatabase(request):
    if request.method == "POST":
        csv_file = request.FILES["csv_file"]
        file_data = csv_file.read().decode("utf-8")	
        lines = file_data.split("\n")
        for line in lines:						
			fields = line.split(",")
            faculty= Faculty(id=fields[0],name=fields[1],email=fields[2],phone_no=fields[3],password=fields[4],date_joined=datetime.now())
            faculty.save()
            return HttpResponse("saved")"""

@login_required(login_url='/login/')
def ChangebookStatus(request):
    if request.method == "GET":
        book = Books.objects.get(id=request.GET.get('bookid'))
        if request.GET.get('cond') == 'add':
            book.available = True
            book.save()
        else:
            book.available = False
            book.save()
    return JsonResponse({"successful":True})
#faculty
@login_required(login_url='/login/')
def BookRequests(request):
    due = 6
    with open('./system/Due.txt','r') as f:
        f.readline()
        f.readline()
        due = int(f.readline())
        print(due)

    if request.method == "POST":
        req = Requests.objects.get(id = request.POST.get('req_id'))
        if (req.date.month+due) >= 12:
                new_month = (req.date.month+due) % 12
                new_year=req.date.year+1
                if new_month==0:
                    new_month = 12
                    new_year = req.date.year
        else:
            new_month = (req.date.month+due)
            new_year = req.date.year
        new_date=date(new_year,new_month,req.date.day)
        issue=issued(book_id=req.book_id,faculty_id=req.faculty_id,issue_date=date.today(),return_date=new_date)
        req.delete()
        issue.save()
        same_book = Requests.objects.filter(book_id=req.book_id)
        for b in same_book:
            b.delete()
        return redirect('/administrator/BookRequest/')
    else:
        req_count = Requests.objects.all()
        t = datetime(date.today().year, date.today().month, date.today().day, 0, 0)
        mydate=t.strftime('%Y-%m-%d')
        allissued = issued.objects.filter(return_date__lt=mydate)
        context={
            'all_requests':Requests.objects.all(),
            'req_count':req_count,
            'overdue':allissued
        }
        return render(request,'administrator/request.html',context=context)

@login_required(login_url='/login/')
def BookIssued(request):
    if request.method == "GET":
        req_count = Requests.objects.all()
        allissued = issued.objects.all().order_by('return_date')
        t = datetime(date.today().year, date.today().month, date.today().day, 0, 0)
        mydate=t.strftime('%Y-%m-%d')
        #allissued = issued.objects.all()
        context={
            'allissued':allissued,
            'req_count':req_count,
            'overdue':issued.objects.filter(return_date__lt=mydate)
        }
        return render(request,'administrator/issued.html',context=context)
    if request.method == "POST":
        if request.POST.get('status') == "return":
            myissue = issued.objects.get(id=request.POST.get('issue_id'))
            myissue.delete()
            return redirect('/administrator/BookIssued/')
        if request.POST.get('status') == "renew":
            myissue = issued.objects.get(id=request.POST.get('issue_id'))
            if (myissue.return_date.month+6) >= 12:
                new_month = (myissue.return_date.month+6) % 12
                new_year=myissue.return_date.year+1
                if new_month==0:
                    new_month = 12
                    new_year = myissue.return_date.year
            else:
                new_month = (myissue.return_date.month+6)
                new_year = myissue.return_date.year
            new_date=date(new_year,new_month,myissue.return_date.day)
            myissue.return_date = new_date
            myissue.save()
            return redirect('/administrator/BookIssued/')

@login_required(login_url='/login/')
def Notify(request):
    t = datetime(date.today().year, date.today().month, date.today().day, 0, 0)
    mydate=t.strftime('%m/%d/%Y')
    subject = 'DeadLine Of Book'
    context={
        'end' : mydate,
    }
    html_message = render_to_string('administrator/mail.html', context)
    plain_message = strip_tags(html_message)
    from_email = 'From <gdthumar@gmail.com>'
    to = 'gdthumar.code@gmail.com'
    mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
    return HttpResponse('Sent')

@login_required(login_url='/login/')
def OverDue(request):
    if request.method == "GET":
        req_count = Requests.objects.all()
        t = datetime(date.today().year, date.today().month, date.today().day, 0, 0)
        mydate=t.strftime('%Y-%m-%d')
        allissued = issued.objects.filter(return_date__lt=mydate)
        context={
            'allissued':allissued,
            'req_count':req_count,
            'today':date.today()
        }
        return render(request,'administrator/overdue.html',context=context)

@login_required(login_url='/login/')
def Send_Notification(request):
    t = datetime(date.today().year, date.today().month, date.today().day, 0, 0)
    mydate=t.strftime('%Y-%m-%d')
    print(mydate)
    allissued = issued.objects.filter(return_date__lt=mydate)
    from_email = 'From <gdthumar@gmail.com>'
    subject = 'DeadLine Of Book'
    to=[]
    for issue in allissued:
        context={
        'end' : issue.return_date,
        }
        to.append(issue.faculty_id.email)
        html_message = render_to_string('administrator/mail.html', context)
        plain_message = strip_tags(html_message)
        to = issue.faculty_id.email
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
    return JsonResponse({"successful":mydate})

@login_required(login_url='/login/')
def ChangeSetting(request):
    if request.method == "GET":
        f=open("./system/Due.txt", "r")
        templines=f.readlines()
        lines = []
        for line in templines:
            lines.append(line)
        print(lines)
        studentduedate=lines[0]
        studentduecharge=lines[1]
        facultyduedate=lines[2]
        facultyduecharge=lines[3]
        #t = date(date.today().year, date.today().month, date.today().day)
        #print(t)
        data={
            'studentduedate':studentduedate,
            'studentduecharge':studentduecharge,
            'facultyduedate':facultyduedate,
            'facultyduecharge':facultyduecharge,
        }
        return JsonResponse(data)
    else:
        studentduedate=request.POST.get('studentduedate')
        studentduecharge=request.POST.get('studentduecharge')
        facultyduedate=request.POST.get('facultyduedate')
        facultyduecharge=request.POST.get('facultyduecharge')
        # 1-> student date 2->charge 3->faculty date 4->charge
        print(studentduedate,studentduecharge)
        print(facultyduedate,facultyduecharge)
        with open('./system/Due.txt','w+') as f:
            f.write(studentduedate+'\n'+ studentduecharge+'\n'+ facultyduedate+'\n'+ facultyduecharge+ '\n')

        return redirect('/administrator/Books/')

def AboutUs(request):
    return render(request,'administrator/aboutus.html')


    




