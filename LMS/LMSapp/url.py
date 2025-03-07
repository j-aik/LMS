from django.contrib import admin
from django.urls import path
from LMSapp import views

app_name = "LMSapp"


urlpatterns = [
    path('',views.home,name="home"),
    path('login',views.u1login,name="u1login"),
    path('delete/<int:id>',views.delete,name="delete"),
    path('active/<int:id>',views.active,name="active"),
]


