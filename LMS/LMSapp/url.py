from django.contrib import admin
from django.urls import path
from LMSapp import views

app_name = "LMSapp"


urlpatterns = [
    path('',views.home,name="home"),
    path('login',views.u1login,name="u1login"),
    path('delete/<int:id>',views.delete,name="delete"),
    path('active/<int:id>',views.active,name="active"),
    path('admin1/<int:id>',views.admin1,name="admin1"),
    path('adminedit/<int:p>',views.adminedit,name="adminedit"),
    path('adminparent',views.adminparent,name="adminparent"),# only for showing class
    path('adminstaff',views.adminstaff,name="adminstaff"),   # only for showing class
    path('adminstudent',views.adminstudent,name="adminstudent"), # only for showing class
    path('adminparent1/<str:p>',views.adminparent1,name="adminparent1"), #taking all the details about parents
    path('adminparentedit/<str:p>/<str:m>',views.adminparentedit,name="adminparentedit"), #editing the parents
    path('adminstaff1/<str:p>',views.adminstaff1,name="adminstaff1"),  #taking all the details about staff
    path('adminstaffedit/<str:p>/<str:m>',views.adminstaffedit,name="adminstaffedit"), # editing the dtaffs
    path('adminstudent1/<str:p>',views.adminstudent1,name="adminstudent1"), #taking all the details about student
    path('adminstudentedit/<str:p>/<str:m>', views.adminstudentedit,name="adminstudentedit"),  # editing the students
    path('createuser', views.createuser,name="createuser"),

]
