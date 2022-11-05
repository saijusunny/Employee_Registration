from django.shortcuts import render, redirect

# Create your views here.
from .models import Employee
from .forms import EmployeeForm

from  django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, auth
from urllib.request import Request


def signup(request):
    return render(request, 'emp/signup.html')

def loginpage(request):
    return render(request, 'emp/login.html')

def usercreate(request):
    if request.method=="POST":
        fname=request.POST['first_name']
        lname=request.POST['last_name']
        username=request.POST['username']
        password=request.POST['password']
        cpass=request.POST['cpassword']
        email=request.POST['email']

        if password==cpass:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'This Username Is Already Exists!!!!!')
                return redirect('signup')
            else:
                user=User.objects.create_user(
                    first_name=fname,
                    last_name=lname,
                    username=username,
                    password=password,
                    email=email,
                )
                user.save()
        else:
            messages.info(request, 'Password doesnot match!!!!!')
            return redirect('signup')
        return redirect('adminlogin')
    else:
        return render(request, 'emp/signup.html')

def adminlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request,username=username, password=password)
       
        if user is not None:
            
            auth.login(request, user)
            messages.info(request, f'Welcome {username}')#pass users name to welcome page
            return redirect('allEmp')
        else:
            messages.info(request, 'invalid username and password, try again')
            return redirect('loginpage')
    else:
        return redirect('loginpage')

@login_required(login_url='adminlogin')
def all_employees(request):
    emps = Employee.objects.filter(user=request.user.id)
    context = {
        'emps': emps
    }
    return render(request, 'emp/index.html', context)


from django.contrib import messages

@login_required(login_url='adminlogin')
def add_employees(request):
    form = EmployeeForm()
    print(request.user.id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            Employee.objects.create(
                user=request.user,
                name=form.cleaned_data['name'],
                pic=form.cleaned_data['pic'],
                mobile=form.cleaned_data['mobile'],
                email=form.cleaned_data['email'],
                salary=form.cleaned_data['salary'],

            )
            messages.add_message(request, messages.INFO, f"Employee {form.cleaned_data.get('name')} has been added")
            return redirect('allEmp')
    context = {
        'form': form,
    }
    return render(request, 'emp/addEmp.html', context)

@login_required(login_url='adminlogin')
def edit_employees(request, id=None):
    
    
        one_emp = Employee.objects.get(id=id)
        form = EmployeeForm(request.POST or None, request.FILES or None, instance=one_emp)
        if form.is_valid():
            form.save()

            messages.add_message(request, messages.INFO, f"{form.cleaned_data.get('name')} has been added")
            return redirect('allEmp')

        context = {
            'form': form,
        }
        return render(request, 'emp/editEmp.html', context)
    

@login_required(login_url='adminlogin')
def one_employee(request, id=None):
    emp = Employee.objects.get(id=id)
    context = {
        'emp': emp
    }
    return render(request, 'emp/viewEmp.html', context)

@login_required(login_url='adminlogin')
def delete_employee(request, id=None):
    emp = Employee.objects.get(id=id)
    if request.method == "POST":
        emp.delete()
        messages.add_message(request, messages.INFO, f"{emp.name} Employee Deleted")
        return redirect('allEmp')
    context = {
        'emp': emp
    }
    return render(request, 'emp/delete.html', context)


@login_required(login_url='adminlogin') #login  session method
def adminlogout(request):
    auth.logout(request)
    return redirect('loginpage')







