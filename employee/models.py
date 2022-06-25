from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class EmployeeList(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    FirstName=models.CharField(max_length=100,blank=False)
    LastName=models.CharField(max_length=100,blank=False)
    Email=models.CharField(max_length=100,blank=False)
    Phone=models.CharField(max_length=100,blank=False)
    Gender=models.CharField(max_length=100,blank=False)
    Age=models.CharField(max_length=100,blank=False)
    Dob=models.CharField(max_length=100,blank=False)
    City=models.CharField(max_length=100,blank=False)

    def __str__(self):
        return str(self.id)
    def get_fullname(self):
        return self.FirstName+" "+self.LastName

class Skill(models.Model):
    user=models.ForeignKey(EmployeeList,on_delete=models.CASCADE)
    skill=models.CharField(max_length=100,blank=False)

    def __str__(self):
        return str(self.id)
