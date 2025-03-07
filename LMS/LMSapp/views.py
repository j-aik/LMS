from django.shortcuts import render,redirect
from django.shortcuts import render,redirect
from LMSapp.models import CustomUser,ClassST,Parent,Staff,Student
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request,'home.html')

def student(request):
    f = request.user.username
    return render(request, 'student.html',{'f':f})

def parent(request):
    f = request.user.username
    return render(request, 'student.html',{'f':f})

def staff(request):
    f = request.user.username
    return render(request, 'staff.html',{'f':f})

def admin1(request):
    f = request.user.username
    f1 = CustomUser.objects.all()
    return render(request, 'admin1.html',{'f':f,'f1':f1})

def u1login(request):
    f = ""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user and user.is_student and user.is_active == True:
            login(request, user)
            return student(request)
        elif user and user.is_parent and user.is_active == True:
            login(request, user)
            return parent(request)
        elif user and user.is_teacher and user.is_active == True:
            login(request, user)
            return staff(request)
        elif user and user.is_admin and user.is_active == True:
            login(request, user)
            return admin1(request)
        else:
            f = "your password is error"
            return render(request, 'login.html', {'f': f})
    return render(request, 'login.html',{'f':f})

def delete(request,id):
    f = CustomUser.objects.get(id=id)
    f.delete()
    return admin1(request)


def active(request,id):
     f = CustomUser.objects.get(id=id)
     if f.is_active == True:
         f.is_active = False
         f.save()
     else:
         f.is_active = True
         f.save()
     return admin1(request)