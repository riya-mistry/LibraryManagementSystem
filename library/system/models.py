from django.db import models
from django.core.validators import RegexValidator
from student.models import Student
from datetime import date,datetime


# Create your models here.

class Books(models.Model):
    sr_no = models.IntegerField()
    id = models.CharField(max_length = 255,primary_key=True)
    title = models.CharField(max_length = 255)
    author = models.CharField(max_length = 255)
    publisher = models.CharField(max_length = 255)
    available = models.BooleanField(default=True)

class Faculty(models.Model):
    id = models.CharField(max_length = 255,primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone_no = models.CharField(max_length=10)
    date_joined = models.DateTimeField(auto_now=True)
    password = models.CharField(max_length=255)
    # any fields you would like to add


class issued(models.Model):
    Faculty_DueCharge = 10
    Faculty_DueDate = 6
    book_id = models.ForeignKey(Books, on_delete=models.CASCADE)
    faculty_id = models.ForeignKey(Faculty, on_delete=models.CASCADE,null=True)
    issue_date = models.DateField(auto_now=True)
    return_date = models.DateField(auto_now=False)


    def calculate_due(self):
        f_date = date(date.today().year,date.today().month,date.today().day)
        return_date = date(self.return_date.year,self.return_date.month ,self.return_date.day)
        return int(((f_date-return_date).days))*int(issued.Faculty_DueCharge)



class Requests(models.Model):
    faculty_id = models.ForeignKey(Faculty, on_delete=models.CASCADE,null=True)
    book_id = models.ForeignKey(Books, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    date= models.DateField(auto_now=True)

class StudentRequest(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE,null=True)
    book_id = models.ForeignKey(Books, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    date= models.DateField(auto_now=True)

class StudentIssued(models.Model):
    Student_DueCharge = 10
    Student_Duedate = 1
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE,null=True)
    book_id = models.ForeignKey(Books, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    date= models.DateField(auto_now=True)
    return_date = models.DateField(auto_now=False)