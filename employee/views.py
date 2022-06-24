from django.shortcuts import redirect, render
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages


def Employees(request):
    return render(request, 'employee/employee.html')


def LoginView(request):
    return render(request, 'employee/login.html')


def SignupView(request):
    if request.method == "POST":
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != "" and password1 == password2:
            sql = "Insert Into User (username,password) Values("
            sql = sql+username+","+password1+")"
            print(sql)
            user = User.objects.raw(sql)
        messages.success(request, "User Create Successfully",
                         extra_tags="signup_complete")
        return redirect('App_Employee:signup')
    return render(request, 'employee/signup.html')


def LogoutView(request):
    logout(request)
    return redirect('App_Employee:login')
