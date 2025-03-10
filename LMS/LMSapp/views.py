from django.shortcuts import render,redirect
from django.shortcuts import render,redirect, get_object_or_404
from LMSapp.models import CustomUser,ClassST,Parent,Staff,Student,Subject
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import UserEditForm,ParentEditForm,StaffEditForm,StudentEditForm
from django.http import JsonResponse

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

def admin1(request,id=0):
    f = request.user.username
    f1 = CustomUser.objects.all()
    print(id)
    try:
        f2 = get_object_or_404(CustomUser, id=id)
        print(f2)
        if request.method == "POST":
           form = UserEditForm(request.POST, instance=f2)
           if form.is_valid():
             form.save()
             return JsonResponse({"success": True})
           else:
               return JsonResponse({"success": False, "errors": form.errors})

        else:
           form = UserEditForm(instance=f2)
           print(form)
           return render(request, 'edit_form.html', {'form': form})
    except:
        return render(request, 'admin1.html', {'f': f, 'f1': f1})


def adminedit(request,p):
        print("it came here ")
        f2 = get_object_or_404(Parent, id=p)
        print(f2)
        if request.method == "POST":
            form = UserEditForm(request.POST, instance=f2)
            if form.is_valid():
                form.save()
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"success": False, "errors": form.errors})

        else:
            form = UserEditForm(instance=f2)
            return render(request, 'parentedit_form.html', {'form': form})

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
            return admin1(request,id=0)
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
     return admin1(request,id=0)

def adminparent(request): # only for showing class
    classst = ClassST.objects.all()
    return render(request,'adminparent.html',{'classst':classst})

def adminparent1(request,p): # for showing class class data about usercreation ,edit
    parent = Parent.objects.filter(class_assigned__name=p)
    return render(request,'adminparent1.html',{'parent':parent})

def adminparentedit(request,p,m): # editform of thr parent
    f3 = Parent.objects.get(id=p)
    user = f3.user
    p = p
    if request.method == "POST":
        user_form = UserEditForm(request.POST, instance=user)
        form = ParentEditForm(request.POST, instance=f3)
        if form.is_valid() and user_form.is_valid():
            user = user_form.save()
            parent = form.save(commit=False)
            parent.user = user
            parent.save()
            return adminparent1(request,m)

    else:
        user_form = UserEditForm(instance=user)
        form = ParentEditForm(instance=f3)
        return render(request, 'parentedit_form.html', {'form': form,'user_form':user_form})


def adminstaff(request): # only for showing class
    classst = ClassST.objects.all()
    return render(request,'adminstaff.html',{'classst':classst})

def adminstaff1(request,p):  # for showing class class data about usercreation ,edit
    staff = Staff.objects.filter(class_assigned__name=p)
    return render(request,'adminstaff1.html',{'staff':staff})


def adminstaffedit(request,p,m):
    f3 = Staff.objects.get(id=p)
    user = f3.user
    if request.method == "POST":
        print(1)
        user_form = UserEditForm(request.POST, instance=user)
        print(2)
        form = StaffEditForm(request.POST, instance=f3)
        print(3)
        print(form.is_valid())
        print("User Form Errors:", user_form.errors)
        print("User Form Valid:", user_form.is_valid())
        print("User Form Errors:", user_form.errors)

        print("Parent Form Valid:", form.is_valid())
        print("Parent Form Errors:", form.errors)
        print(user_form.is_valid())
        if form.is_valid() and user_form.is_valid():
            user = user_form.save()
            parent = form.save(commit=False)
            parent.user = user
            parent.save()
            return adminstaff1(request,m)

    else:
        user_form = UserEditForm(instance=user)
        form = ParentEditForm(instance=f3)
    return render(request,'staff_editform.html',{'form': form,'user_form':user_form})

def adminstudentedit(request,p,m):
    f3 = Student.objects.get(id=p)
    user = f3.user
    if request.method == "POST":
        user_form = UserEditForm(request.POST, instance=user)
        form = StudentEditForm(request.POST, instance=f3)
        print("User Form Errors:", user_form.errors)
        print("Student Form Errors:", form.errors)
        if user_form.is_valid() and form.is_valid() :
            user_form.save()
            form.save()
            return adminstudent1(request,m)
        else:
            return adminstudent1(request,m)
    else:
        user_form = UserEditForm(instance=user)
        form = StudentEditForm(instance=f3)
        print(form)
        return render(request, 'studentedit_form.html', {'form': form,'user_form':user_form})



def adminstudent(request): # only for showing class
    classst = ClassST.objects.all()
    return render(request,'adminstudent.html',{'classst':classst})

def adminstudent1(request,p):  # for showing class class data about usercreation ,edit
    student = Student.objects.filter(class_assigned__name=p)
    return render(request,'adminstudent1.html',{'student':student})


def createuser(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        is_student = request.POST["is_student"]
        is_parent = request.POST["is_parent"]
        is_admin = request.POST["is_admin"]
        is_teacher = request.POST["is_teacher"]
        dob = request.POST["date_of_birth"]
        class_assigned = request.POST["class_assigned"]
        attendence_percentage =  request.POST["attendence_percentage"]
        password = "1234"
        phone_number = request.POST["phone_number"]
        pusername = request.POST["pusername"]
        address    = request.POST["address"]
        designation = request.POST['designation']
        subject = request.POST['subject']
        is_student = request.POST.get("is_student") == True
        is_parent = request.POST.get("is_parent") == True
        is_admin = request.POST.get("is_admin") == True

        print(f"Student: {is_student}, Parent: {is_parent}, Admin: {is_admin}")

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_student=is_student,
            is_parent=is_parent,
            is_admin=is_admin,
            is_teacher=is_teacher
        )
        if is_student:
            date_of_birth = request.POST.get["date_of_birth"]
            class_assigned_id = request.POST.get["class_assigned"]
            parent_id = request.POST.get["parent"]

            class_assigned = ClassST.objects.create(name=class_assigned_id)
            class_assigned.save()
            is_parent = True,
            puser = CustomUser.objects.create_user(
                username=pusername,
                email=email,
                password=password,
                is_student=is_student,
                is_parent=is_parent,
                is_admin=is_admin,
                is_teacher=is_teacher
            )
            parent = Parent.objects.create(
                user=puser,
                phone_number=phone_number,
                address=address
            )
            s = Student.objects.create(
                user=user,
                date_of_birth=date_of_birth,
                class_assigned=class_assigned,
                parent=parent
            )
            puser.save()


            parent.save()

            s.save()
        elif is_parent:
            phone_number = request.POST.get["phone_number"]
            address = request.POST.get["address"]


            class_assigned = ClassST.objects.create(name=class_assigned)
            class_assigned.save()
            p = Parent.objects.create(
                user=user,
                phone_number=phone_number,
                address=address,
                class_assigned=class_assigned
            )
            p.save()
        elif is_teacher:
            designation = request.POST["designation"]
            phone_number = request.POST["phone_number"]
            class_assigned_id = request.POST["class_assigned"]
            subject_id = request.POST["subject"]
            class_assigned = ClassST.objects.create(name=class_assigned_id)
            class_assigned.save()

            subject = Subject.objects.get(id=subject_id) if subject_id else None

            p = Staff.objects.create(
                user=user,
                designation=designation,
                phone_number=phone_number,
                class_assigned=class_assigned,
                subject=subject
            )
            p.save()

    return render(request, 'newusercreation.html', {'student': student})