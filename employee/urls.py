from django.urls import path
from employee import views
app_name = 'App_Employee'

urlpatterns = [
    path('', views.Employees, name='employeelist'),
    path('login', views.LoginView, name="login"),
    path('signup', views.SignupView, name="signup"),
    path('logout', views.LogoutView, name="logout"),
    path('add', views.AddEmployee, name="addemployee"),
    path('details/<int:id>', views.SingleEmployee, name="details"),
    path('edit/<int:id>', views.EditEmployee, name="editemployee"),
    path('delete', views.DeleteEmployee, name="deleteemployee"),
]
