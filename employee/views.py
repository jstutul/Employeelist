from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import connection
from datetime import datetime
from employee.models import EmployeeList
from django.contrib.auth.decorators import login_required

@login_required(login_url='App_Employee:login')
def Employees(request):
    ps = 4
    pn = 1
    name=city=minage=maxage=gender=mindate=maxdate=""
    if request.method == "POST":
        name=request.POST.get('Formname',"")
        city=request.POST.get('FormCity',"")
        minage=request.POST.get('FormMinAge',"")
        maxage=request.POST.get('FormMaxAge',"")
        gender=request.POST.get('FormGender',"")
        mindate=request.POST.get('FormMinDate',"")
        maxdate=request.POST.get('FormMaxDate',"")
        
        qex = int(request.POST["PageNo"])
        if qex != "":
            pn = qex
    ExcludeRecors = (pn-1)*ps
    sql1="Select id,FirstName,LastName,Email,Gender,Phone,Dob,Age,City, count(1) over() TC From employee_employeelist "
    sql2=" user_id='"+str(request.user.id)+"' ORDER BY id DESC LIMIT " + str(ps) + " OFFSET "+str(ExcludeRecors)
    SqlQuery = ""
    if name!="":
        SqlQuery=SqlQuery + "( FirstName Like '%"+ name +"%' OR LastName Like '%"+name+"%' ) "
    if city!="" and city!="Select":
        if SqlQuery !="":
            SqlQuery=SqlQuery + " AND "
        SqlQuery=SqlQuery + " City='" + city + "'"
    if minage!="" and minage!="Min Age":
        if SqlQuery !="":
            SqlQuery=SqlQuery + " AND "
        SqlQuery=SqlQuery + "  Age>='" + minage + "' "    
    if maxage!="" and maxage!="Max Age":
        if SqlQuery !="":
            SqlQuery=SqlQuery + " AND "
        SqlQuery=SqlQuery + "  Age<='" + maxage + "' "    
    if mindate!="":
        if SqlQuery !="":
            SqlQuery=SqlQuery + " AND "
        SqlQuery=SqlQuery + "  Dob>='" + mindate + "' "  
    if maxdate!="":
        if SqlQuery !="":
            SqlQuery=SqlQuery + " AND "
        SqlQuery=SqlQuery + "  Dob<='" + maxdate + "' "  
    if gender!="":
        if SqlQuery !="":
            SqlQuery=SqlQuery+" AND "
        SqlQuery=SqlQuery + " Gender='" + gender + "'"
     

    if SqlQuery != "":
        SqlQuery =sql1+ " where "+SqlQuery+" AND "+sql2
    else:
        SqlQuery =sql1+ " where "+sql2
    print(SqlQuery)
    with connection.cursor() as cursor:
        cursor.execute(SqlQuery )
        all_employees = cursor.fetchall()
    PageCount = 0

    if len(all_employees) != 0:
        Totaldata = all_employees[0][9]
        ExtraPage = (Totaldata / ps)
        PageCount = round(Totaldata / ps)
        print(ExtraPage, PageCount)
        if ExtraPage > PageCount and PageCount >= 1:
            PageCount = PageCount+1
    print(PageCount)
    context = {
        'all_employees': all_employees,
        'pn': pn,
        'range': range(1, PageCount+1),
        'PageCount': PageCount,
        'name':name,
        'city':city,
        'minage':minage,
        'maxage':maxage,
        'mindate':mindate,
        'maxdate':maxdate,
        'minagerange':range(18,40),
        'maxagerange':range(30,80),
    }
    return render(request, 'employee/employee.html', context)


def LoginView(request):
    if request.user.is_authenticated:
        return redirect('App_Employee:employeelist')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('App_Employee:employeelist')
            else:
                messages.info(
                    request, "Enter correct username and password", extra_tags="login_error")
                return redirect('App_Employee:login')
    return render(request, 'employee/login.html')


def SignupView(request):
    if request.method == "POST":
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != "" and password1 == password2:
            user = User.objects.create_user(
                username=username, password=password1)
            if user:
                messages.success(
                    request, "User Create Successfully", extra_tags="signup_complete")
            return redirect('App_Employee:signup')
    return render(request, 'employee/signup.html')


def LogoutView(request):
    logout(request)
    return redirect('App_Employee:login')


def calculateAge(birthDate):
    birthDate = datetime.strptime(birthDate, "%Y-%m-%d")
    days_in_year = 365.2425
    age = int((datetime.today() - birthDate).days / days_in_year)
    return age

@login_required(login_url='App_Employee:login')
def AddEmployee(request):

    if request.method == "POST":
        FormFirstName = request.POST.get("FormFirstName")
        FormLastName = request.POST.get("FormLastName", "")
        FormEmail = request.POST.get("FormEmail", "")
        FormPhone = request.POST.get("FormPhone", "")
        FormDob = request.POST["FormDob"]
        FormGender = request.POST.get("FormGender", "male")
        FormCity = request.POST.get("FormCity", "")
        FormAge = calculateAge(FormDob)
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO employee_employeelist (user_id,FirstName,LastName,Email,Gender,Phone,Dob,Age,City) VALUES('"+str(request.user.id) +
                           "','"+FormFirstName+"','"+FormLastName+"','"+FormEmail+"','"+FormGender+"','"+FormPhone+"','"+FormDob+"','"+str(FormAge)+"','"+FormCity+"')")
            newID = cursor.lastrowid

            ForkSkills = request.POST.getlist('Formskills')
            skillSql = "INSERT INTO  employee_skill (user_id,skill) VALUES "
            sql = ""
            for sk in ForkSkills:
                if sql != "":
                    sql = sql+","
                sql = sql+"( '"+str(newID)+"','"+sk+"') "
            finalskillSql = skillSql+sql
            cursor.execute(finalskillSql)
            cursor.close()
            messages.success(request, "Data Insert Successfully",
                             extra_tags="data_insert")
            return redirect('App_Employee:addemployee')

    return render(request, "employee/addemployee.html")

@login_required(login_url='App_Employee:login')
def SingleEmployee(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT E.id, E.FirstName ,E.LastName,E.Email,E.Phone,E.Gender,E.Age,E.Dob,E.City,S.skill,S.id, S.user_id FROM employee_employeelist E inner join employee_skill s on E.id = s.user_id Where E.id='"+str(id)+"'AND E.user_id='"+str(request.user.id)+"'")
        single_employee = cursor.fetchall()
    context = {
        'single_employee': single_employee,
    }
    return render(request, 'employee/singleemployee.html', context)

@login_required(login_url='App_Employee:login')
def EditEmployee(request,id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT E.id, E.FirstName ,E.LastName,E.Email,E.Phone,E.Gender,E.Age,E.Dob,E.City,S.skill,S.id, S.user_id FROM employee_employeelist E inner join employee_skill s on E.id = s.user_id Where E.id='"+str(id)+"'AND E.user_id='"+str(request.user.id)+"'")
        single_employee = cursor.fetchall()
        cursor.close()
    print(single_employee)    
    if request.method=="POST":
        FormFirstName = request.POST.get("FormFirstName",single_employee[0][1])
        FormLastName = request.POST.get("FormLastName", single_employee[0][2])
        FormEmail = request.POST.get("FormEmail", single_employee[0][3])
        FormPhone = request.POST.get("FormPhone", single_employee[0][4])
        FormDob = request.POST["FormDob"]
        FormGender = request.POST.get("FormGender", single_employee[0][5])
        FormCity = request.POST.get("FormCity", single_employee[0][8])
        FormAge = calculateAge(FormDob)
        with connection.cursor() as cursor:
            cursor.execute("UPDATE employee_employeelist SET FirstName='"+FormFirstName+"',LastName='"+FormLastName+"',Email='"+FormEmail+"',Gender='"+FormGender+"',Phone='"+FormPhone+"',Dob='"+FormDob+"',Age='"+str(FormAge)+"',City='"+FormCity+"' WHERE id='"+str(id)+"' AND user_id='"+str(request.user.id)+"'")
            cursor.execute("Delete From employee_skill Where user_id='"+str(id)+"'")
            cursor.close()
        ForkSkills = request.POST.getlist('Formskills')
        skillSql = "INSERT INTO  employee_skill (user_id,skill) VALUES "
        sql = ""
        for sk in ForkSkills:
            if sql != "":
                sql = sql+","
            sql = sql+"( '"+str(id)+"','"+sk+"') "
        finalskillSql = skillSql+sql
        with connection.cursor() as cursor:
            cursor.execute(finalskillSql)
            cursor.close()
        messages.success(request, "Data Update Successfully",
                         extra_tags="data_update")
        return redirect('./%d'%id)
    context = {
        'single_employee': single_employee,
    }
    return render(request,"employee/editemployee.html",context)


def DeleteEmployee(request):
    
    if request.method=="POST":
        emp_id=request.POST["emp_id"]
        sql="SELECT E.id,E.user_id FROM employee_employeelist E inner join employee_skill s on E.id = s.user_id WHERE E.user_id ="+str(request.user.id)+" AND E.id ="+str(emp_id)
        with connection.cursor() as cursor:
            cursor.execute(sql)
            single_employee = cursor.fetchone()
            cursor.close()
        print(single_employee)  
        if len(single_employee)>0:
            with connection.cursor() as cursor:
                print("eid=",single_employee[0])

                cursor.execute("Delete From employee_skill Where user_id="+str(single_employee[0]))
                cursor.execute("Delete From employee_employeelist Where id="+str(single_employee[0]))
                cursor.close()
                messages.success(request, "Data Delte Successfully",
                         extra_tags="data_delete")
        else:
            messages.success(request, "Something went wrong",
                         extra_tags="data_delete")
        return redirect('App_Employee:employeelist')