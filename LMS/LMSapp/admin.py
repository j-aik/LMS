from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from LMSapp.models import ClassST,CustomUser,Parent,Staff,Student,Subject

admin.site.register(ClassST)
admin.site.register(CustomUser)
admin.site.register(Parent)
admin.site.register(Staff)
admin.site.register(Student)
admin.site.register(Subject)