from django.shortcuts import render,redirect
from django.shortcuts import render,redirect, get_object_or_404
from LMSapp.models import CustomUser,ClassST,Parent,Staff,Student,Subject,Assigned
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
    f1 = Staff.objects.filter(user__username = f)
    h = []
    h1 = set()
    for i in f1:
            h.append(i.subject)
            h1.add(i.class_assigned.name)
            print(h1)
    h1 = list(h1)
    return render(request, 'staff.html',{'f':f,'f1':f1,'h1':h1})


def staffstudent(request):
    f = request.user.username
    f1 = Staff.objects.filter(user__username=f)
    h = []
    h1 = []
    for i in f1:
            h.append(i.subject)
            h1.append(i.class_assigned.name)
    print(h1,"this is h1")
    print(h,"this is h")
    for i in f1:

            f3 = i
            f6 = ClassST.objects.filter(name=i.class_assigned.name).first()

            # Check if an Assigned object already exists
            f7, created = Assigned.objects.get_or_create(
                staff=f3,
                class_assigned=f6,
            )
            assigned_subjects = list(f7.subject.all())


            print(assigned_subjects, "Current subjects in f7")



            for subj in h:
               if subj not in assigned_subjects:

                   f7.subject.add(subj)
                   f7.save()

    return render(request, 'staff.html', {'f': f, 'f1': f1 , 'h1':h1})


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
        if user_form.is_valid() and form.is_valid():
            print(form.cleaned_data)
            user_form.save()
            form.save()
            print("is saved")

            return adminstudent1(request,m)
        else:
            return adminstudent1(request,m)
    else:
        user_form = UserEditForm(instance=user)
        form = StudentEditForm(instance=f3)

        return render(request, 'studentedit_form.html', {'form': form,'user_form':user_form})



def adminstudent(request): # only for showing class
    classst = ClassST.objects.all()
    return render(request,'adminstudent.html',{'classst':classst})

def adminstudent1(request,p):  # for showing class class data about usercreation ,edit
    student = Student.objects.filter(class_assigned__name=p)
    return render(request,'adminstudent1.html',{'student':student})


def createuser(request):
    classst = ClassST.objects.all()
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        dob = request.POST["date_of_birth"]
        attendence_percentage =  request.POST["attendence_percentage"]
        password = "1234"
        phone_number = request.POST["phone_number"]
        pusername = request.POST["pusername"]
        address    = request.POST["address"]
        designation = request.POST['designation']
        subject = request.POST['subject']
        is_student = request.POST.get("is_student") is not None
        is_parent = request.POST.get("is_parent") is not None
        is_teacher = request.POST.get("is_teacher") is not None
        try:
            class_assigned  =  request.POST['classst']
            class_assigned = ClassST.objects.get(id=class_assigned)
        except:
            class_assigned = request.POST["class_assigned"]
            class_assigned = ClassST.objects.create(name=class_assigned)

        print(f"Student: {is_student}, Parent: {is_parent}, teacher: {is_teacher}")


        print(is_student, "student tag")
        if is_student:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_student=is_student,
                is_parent=is_parent,
                is_teacher=is_teacher
            )
            print(is_student,"student tag")
            date_of_birth = request.POST["date_of_birth"]



            puser = CustomUser.objects.create_user(
                username=pusername,
                email=email,
                password=password,
                is_student=is_student,
                is_parent=is_parent,
                is_teacher=is_teacher
            )

            parent = Parent.objects.create(
                user=puser,
                phone_number=phone_number,
                address=address,
                class_assigned = class_assigned
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
            print(is_parent, "parent tag")
        elif is_parent:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_student=is_student,
                is_parent=is_parent,
                is_teacher=is_teacher
            )
            print(is_parent, "parent tag")
            phone_number = request.POST["phone_number"]
            address = request.POST["address"]



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
            subject_id = request.POST["subject"]
            h = Subject.objects.all()
            u = []
            for i in h:
                u.append(i.subject)
            if subject_id in u:
                d =  Subject.objects.get(subject=subject_id)
            else:
                d = Subject.objects.create(subject=subject_id)
            # try:
            print(username,"This is username")
            try:
               try:
                 user = CustomUser.objects.get(username=username)
                 p = Staff.objects.get(
                      user=user,
                      class_assigned=class_assigned
                  )
                 p.subject.add(d)
                 p.save()
                 d.save()
               except:
                   user = CustomUser.objects.get(username=username)
                   p = Staff.objects.create(
                       user=user,
                       class_assigned=class_assigned
                   )
                   p.subject.add(d)
                   p.save()
                   d.save()
            except:
                user = CustomUser.objects.create_user(
                  username=username,
                  email=email,
                  password=password,
                  is_student=is_student,
                 is_parent=is_parent,
                 is_teacher=is_teacher
                 )
                p = Staff.objects.create(
                user=user,
                designation=designation,
                phone_number=phone_number,
                class_assigned = class_assigned
                 )
                p.subject.set([d])
                p.save()
                d.save()


    return render(request, 'newusercreation.html', {'student': student,'classst': classst})


def staffclass(request,p):
    print(p)
    g = request.user
    l = Staff.objects.get(user=g,class_assigned__name=p)
    print(l)
    return render(request, 'staffsubject.html', {'l':l})