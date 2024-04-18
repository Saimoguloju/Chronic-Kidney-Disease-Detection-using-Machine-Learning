"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views as myapp
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', myapp.index, name='index'),
    path('logout/',myapp.logout,name='logout'),
    path('userlogin/',myapp.userlogin,name='userlogin'),
    path('userregister/',myapp.userregister,name='userregister'),
    path('userlogincheck/',myapp.userlogincheck,name='userlogincheck'),
    path('adddata/', myapp.adddata, name='adddata'),
    path('spamreport/',myapp.checkspam,name='report'),
    path('adddata/', myapp.adddata, name='adddata'),
    path('adminlogin1/',myapp.adminlogin1,name='adminlogin1'),
    path('adminloginentered/',myapp.adminloginentered,name='adminloginentered'),
    path('userdetails/',myapp.userdetails,name='userdetails'),
    path('activateuser/',myapp.activateuser,name='activateuser'),
    path('contact/',myapp.contact,name='contact'),
    path('about/',myapp.about,name='about'),
    path('home/',myapp.home,name='home'),
    path('contact1/',myapp.contact1,name='contact1'),
    path('aboutproject/',myapp.aboutproject,name='aboutproject'),
    path('recommendation/',myapp.recommendation,name='recommendation'),
    path('initialstage/',myapp.initial_stage, name='initialstage'),
    path('firststage/', myapp.first_stage, name='firststage'),
    path('secondstage/', myapp.second_stage, name='secondstage'),
    path('thirdstage/',myapp.third_stage, name='thirdstage'),
    path('fourthstage/',myapp.fourth_stage, name='fourthstage'),
]
