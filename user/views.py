import datetime
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login as login_user, logout as logout_user
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.sessions.models import Session


from user.models import User
# from logaktifitas.models import Logaktifitas
date_now = datetime.datetime.now()

def login(request):
    # if request.user.is_authenticated:
    #     return redirect('login')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.role == "Admin":
            login_user(request, user)
            # Logaktifitas.objects.create(pegawai=request.user, activity="Login" , date=date_now)
            messages.success(request, 'Success login')
            return redirect('user:manageuser')
            
        elif user is not None and user.role == "Kantin":
            login_user(request, user)
            # Logaktifitas.objects.create(pegawai=request.user, activity="Login" , date=date_now)
            messages.success(request, 'Success login')
            return redirect('kantin:managemenu')
            
        elif user is not None and user.role == "Mahasiswa":
            login_user(request, user)
            # Logaktifitas.objects.create(pegawai=request.user, activity="Login" , date=date_now)
            messages.success(request, 'Success login')
            return redirect('pesanan:home')
  
        else:
            messages.error(request, 'Invalid credential')
    return render(request, 'login.html')

@login_required
def manageUser(request):
    if request.user.role != "Admin":
        return HttpResponse("Anda Bukan Admin")
    
    s = Session.objects.all()
    
    context = {
        'user' : User.objects.all()
    }
    return render(request, 'manageUser.html', context)

@login_required
def tambahUser(request):
    if request.user.role != 'Admin':
            return HttpResponse('Adnda bukan admin')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        hash_password = make_password(password)

        try:
            User.objects.create(
            username=username, password=hash_password, text_password=password, role=role)                
            # Logaktifitas.objects.create(pegawai=request.user, activity="Menambahkan user baru dengan nama %s"%username , date=date_now)
            messages.success(request, 'Success membuat user baru')
        except:
            messages.error(request, 'Failed membuat User Baru' 'Failed membuat pegawai baru')
    return redirect('user:manageuser')

@login_required
def updateUser(request):
    if request.user.role != 'Admin':
        return HttpResponse('Anda bukan admin')
    if request.method == "POST":
        userID = request.POST.get('id')
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        hash_password = make_password(password)

        user_obj = User.objects.get(id=userID)
        user_obj.username = username
        user_obj.password = hash_password
        user_obj.text_password = password
        user_obj.role = role

        try:
            user_obj.save()
            # Logaktifitas.objects.create(pegawai=request.user, activity="Mengupdate user %s"%username , date=date_now)
            messages.success(request, 'Success update pegawai')
        except:
            messages.error(request, 'Failed update pegawai')
    return redirect('user:manageuser')

@login_required
def deleteUser(request):
    if request.user.role != 'Admin':
        return HttpResponse('Anda bukan admin')

    if request.method == "POST":
        try:
            userName = User.objects.get(id=request.POST.get('id'))
            User.objects.filter(id=request.POST.get('id')).delete()
            # Logaktifitas.objects.create(pegawai=request.user, activity="Mendelete user %s"%userName , date=date_now)
            messages.success(request, 'Success delete pegawai')
        except:
            messages.error(request, 'Failed delete pegawai')
    return redirect('user:manageuser')
    

@login_required
def logout(request):
    logout_user(request)
    return redirect('login')