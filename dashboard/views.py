from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from main import models


# Autentifikatsiya
def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard:index')
        else:
            error_message = "Username or password is incorrect"
            return render(request, 'auth/login.html', {'error_message': error_message})
    return render(request, 'auth/login.html')


def log_out(request):
    logout(request)
    return redirect('dashboard:log_in')


# Profilni tahrirlash
@login_required(login_url='dashboard:log_in')
def edit_profile(request, id):
    user = get_object_or_404(User, id=id)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        
        if password:
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            if new_password == confirm_password:
                user.set_password(new_password)
            else:
                error_message = "Passwords do not match"
                return render(request, 'dashboard/profile.html', {'user': user, 'error_message': error_message})
        
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        
        return redirect('dashboard:index')
    
    return render(request, 'dashboard/profile.html', {'user': user})


# Admin panel bosh sahifasi
@login_required(login_url='dashboard:log_in')
def index(request):
    user_count = User.objects.count()
    staff_count = models.Staff.objects.count()
    
    context = {
        'user_count': user_count,
        'staff_count': staff_count,
    }
    
    return render(request, 'dashboard/index.html', context)


# Xodimlar
@login_required(login_url='dashboard:log_in')
def create_staff(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        models.Staff.objects.create(first_name=first_name, last_name=last_name)
        return redirect('dashboard:list_staff')
    return render(request, 'dashboard/staff/create.html')


@login_required(login_url='dashboard:log_in')
def list_staff(request):
    staff = models.Staff.objects.all()
    context = {
        'staff': staff,
    }
    return render(request, 'dashboard/staff/list.html', context)


@login_required(login_url='dashboard:log_in')
def update_staff(request, id):
    staff = get_object_or_404(models.Staff, id=id)
    
    if request.method == 'POST':
        staff.first_name = request.POST['first_name']
        staff.last_name = request.POST['last_name']
        staff.save()
        return redirect('dashboard:list_staff')
    
    return render(request, 'dashboard/staff/update.html', {'staff': staff})


@login_required(login_url='dashboard:log_in')
def delete_staff(request, id):
    staff = get_object_or_404(models.Staff, id=id)
    staff.delete()
    return redirect('dashboard:list_staff')


# Kelishlar
@login_required(login_url='dashboard:log_in')
def list_attendance(request):
    attendance = models.Attendance.objects.all()
    context = {
        'attendance': attendance,
    }
    return render(request, 'dashboard/attendance/list.html', context)
