
from django.contrib import admin
from django.urls import path
from plantdsapp import views as plantdsapp


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', plantdsapp.index, name='index'),
    path('logout/',plantdsapp.logout,name='logout'),
    path('userlogin/',plantdsapp.userlogin,name='userlogin'),
    path('userregister/',plantdsapp.userregister,name='userregister'),
    path('userlogincheck/',plantdsapp.userlogincheck,name='userlogincheck'),
    path('adddata/', plantdsapp.adddata, name='adddata'),
    path('spamreport/',plantdsapp.checkspam,name='report'),
    path('adddata/', plantdsapp.adddata, name='adddata'),
    path('adminlogin1/',plantdsapp.adminlogin1,name='adminlogin1'),
    path('adminloginentered/',plantdsapp.adminloginentered,name='adminloginentered'),
    path('userdetails/',plantdsapp.userdetails,name='userdetails'),
    path('activateuser/',plantdsapp.activateuser,name='activateuser'),


]


