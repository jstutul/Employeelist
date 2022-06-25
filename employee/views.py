from django.shortcuts import redirect, render
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import connection
from datetime import datetime
from employee.models import EmployeeList

def Employees(request):
    ps=4
    pn=1
    
    if request.method=="POST":
        qex=request.POST["PageNo"]
        if qex !="":
            pn=qex
    ExcludeRecors=(pn-1)*ps 

    with connection.cursor() as cursor:
        cursor.execute("Select id,FirstName,LastName,Email,Gender,Phone,Dob,Age,City, count(1) over() TC From employee_employeelist ORDER BY id DESC LIMIT "+str(ps)+ " OFFSET "+str(ExcludeRecors))
        all_employees=cursor.fetchall()
    PageCount= 0    
    if all_employees!="":
        Totaldata=all_employees[0][9]
        ExtraPage=( Totaldata/ 8)
        PageCount=round( Totaldata / 8) 
        if ExtraPage >PageCount and  PageCount >=1:
            PageCount=PageCount+1
          
    context={
        'all_employees':all_employees,
        'pn':pn,
        'range':range(PageCount),
        'PageCount':PageCount,
    }
    return render(request, 'employee/employee.html',context)


def LoginView(request):
    if request.user.is_authenticated:
        return redirect('App_Employee:employeelist')
    else:
        if request.method == 'POST':
            username=request.POST['username']
            password=request.POST['password']
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('App_Employee:employeelist')
            else:
                messages.info(request,"Enter correct username and password",extra_tags="login_error")
                return redirect('App_Employee:login')
    return render(request, 'employee/login.html')


def SignupView(request):
    if request.method == "POST":
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != "" and password1 == password2:
            user = User.objects.create_user(username=username,password=password1)
            if user:
                messages.success(request, "User Create Successfully",extra_tags="signup_complete")
            return redirect('App_Employee:signup')
    return render(request, 'employee/signup.html')


def LogoutView(request):
    logout(request)
    return redirect('App_Employee:login')

 
def calculateAge(birthDate):
    birthDate= datetime.strptime(birthDate, "%Y-%m-%d")
    days_in_year = 365.2425   
    age = int((datetime.today() - birthDate).days / days_in_year)
    return age
         

def AddEmployee(request):



    if request.method=="POST":
        FormFirstName=request.POST.get("FormFirstName")
        FormLastName=request.POST.get("FormLastName","")
        FormEmail=request.POST.get("FormEmail","")
        FormPhone=request.POST.get("FormPhone","")
        FormDob=request.POST["FormDob"]
        FormGender=request.POST.get("FormGender","male")
        FormCity=request.POST.get("FormCity","")
        qex=request.POST["PageNo"]
        if qex !="":
            pn=qex
        ExcludeRecors=(pn-1)*ps 
        FormAge=calculateAge(FormDob)
        print(ExcludeRecors,ps)
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO employee_employeelist (user_id,FirstName,LastName,Email,Gender,Phone,Dob,Age,City) VALUES('"+str(request.user.id)+"','"+FormFirstName+"','"+FormLastName+"','"+FormEmail+"','"+FormGender+"','"+FormPhone+"','"+FormDob+"','"+str(FormAge)+"','"+FormCity+"')")
            newID=cursor.lastrowid

            ForkSkills=request.POST.getlist('Formskills')
            skillSql="INSERT INTO  employee_skill (user_id,skill) VALUES "
            sql=""
            for sk in ForkSkills:
                if sql !="":
                    sql=sql+","
                sql=sql+"( '"+str(newID)+"','"+sk+"') "
            finalskillSql=skillSql+sql
            cursor.execute(finalskillSql)
            cursor.close()
            messages.success(request,"Data Insert Successfully",extra_tags="data_insert")
            return redirect('App_Employee:addemployee')


    return render(request,"employee/addemployee.html")