from django.db import models

# Create your models here.

class Student(models.Model):
    id = models.CharField(max_length = 255,primary_key=True)
    name = models.CharField(max_length=255,default="dummy")
    email = models.EmailField(max_length=255, unique=True)
    phone_no = models.CharField(max_length=10)
    password = models.CharField(max_length=255)
    branch = models.CharField(max_length=2,default="CE")