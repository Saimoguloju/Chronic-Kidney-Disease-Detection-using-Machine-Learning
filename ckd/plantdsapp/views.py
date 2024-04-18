
from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib import messages
from django.shortcuts import render, HttpResponse
from django_pandas.io import read_frame




import numpy as np
import pandas as pd
import joblib

#from keras.models import load_model




def adminlogin1(request):
    return render(request, "adminlogin.html")

def adminloginentered(request):
    if request.method == 'POST':
        uname=request.POST['uname']
        passwd=request.POST['upasswd']
        if uname =='admin' and passwd =='admin':
            return render(request,"adminloginentered.html")
        else:
            return HttpResponse("invalied credentials")
    return render(request, "adminloginentered.html")


def userdetails(request):
    qs=userModel.objects.all()
    return render(request,"userdetails.html",{"qs":qs})

def activateuser(request):
    if request.method =='GET':
        uname=request.GET.get('pid')
        print(uname)
        status='Activated'
        print("pid=",uname,"status=",status)
        userModel.objects.filter(id=uname).update(status=status)
        qs=userModel.objects.all()
        return render(request,"userdetails.html",{"qs":qs})

# Create your views here.

def index(request):
    return render(request,'index.html')

def logout(request):
    return render(request, "index.html")

def userlogin(request):
    return render(request,'userlogin.html')

def userregister(request):
    if request.method=='POST':
        form1=userForm(request.POST)
        if form1.is_valid():
            form1.save()
            print("succesfully saved the data")
            return render(request, "userlogin.html")
            #return HttpResponse("registreration succesfully completed")
        else:
            print("form not valied")
            return HttpResponse("form not valid")
    else:
        form=userForm()
        return render(request,"userregister.html",{"form":form})


def userlogincheck(request):
    if request.method == 'POST':
        sname = request.POST['email']
        print(sname)
        spasswd = request.POST['upasswd']
        print(spasswd)
        try:
            check = userModel.objects.get(email=sname,passwd=spasswd)
            # print('usid',usid,'pswd',pswd)
            print(check)
            # request.session['name'] = check.name
            # print("name",check.name)
            status = check.status
            print('status',status)
            if status == "Activated":
                request.session['email'] = check.email
                return render(request, 'userpage.html')
            else:
                messages.success(request,'user is not activated')
                return render(request, 'userlogin.html')
        except Exception as e:
            print('Exception is ',str(e))
            pass
        messages.success(request,'Invalid name and password')
        return render(request,'userlogin.html')





import joblib

model = joblib.load('model/DT.joblib')
loaded_scaler = joblib.load('model/scaler.joblib')

columns=['age', 'blood_pressure', 'specific_gravity', 'albumin', 'sugar',
       'red_blood_cells', 'pus_cell', 'pus_cell_clumps', 'bacteria',
       'blood_glucose_random', 'blood_urea', 'serum_creatinine', 'sodium',
       'potassium', 'haemoglobin', 'packed_cell_volume',
       'white_blood_cell_count', 'red_blood_cell_count', 'hypertension',
       'diabetes_mellitus', 'coronary_artery_disease', 'appetite',
       'peda_edema', 'aanemia','eGFR']

cat_cols = ['red_blood_cells', 'pus_cell', 'pus_cell_clumps', 'bacteria', 'hypertension', 'diabetes_mellitus', 'coronary_artery_disease', 'appetite', 'peda_edema', 'aanemia']

# Load LabelEncoder models
loaded_label_encoders = {}
for column in cat_cols:
    model_file_path = f"model/{column}_label_encoder.joblib"  
    loaded_label_encoders[column] = joblib.load(model_file_path)



def checkspam(request):
    if request.method == 'POST':
        age = request.POST.get('age')
        bp = request.POST.get('bp')
        sg = request.POST.get('sg')
        al = request.POST.get('al')
        su = request.POST.get('su')
        rbc = request.POST.get('rbc')
        pc = request.POST.get('pc')
        pcc = request.POST.get('pcc')
        ba = request.POST.get('ba')
        bgr = request.POST.get('bgr')
        bu = request.POST.get('bu')
        sc = request.POST.get('sc')
        sod = request.POST.get('sod')
        pot = request.POST.get('pot')
        hemo = request.POST.get('hemo')
        pcv = request.POST.get('pcv')
        wc = request.POST.get('wc')
        rc = request.POST.get('rc')
        htn = request.POST.get('htn')
        dm = request.POST.get('dm')
        cad = request.POST.get('cad')
        appet = request.POST.get('appet')
        pe = request.POST.get('pe')
        ane = request.POST.get('ane')
        eGFR = request.POST.get('eGFR')
       
        d = {'age':[age], 'blood_pressure':[bp], 'specific_gravity':[sg], 'albumin':[al], 'sugar':[su], 'red_blood_cells':[rbc], 'pus_cell':[pc], 'pus_cell_clumps':[pcc], 'bacteria':[ba], 'blood_glucose_random':[bgr],
       'blood_urea':[bu], 'serum_creatinine':[sc], 'sodium':[sod], 'potassium':[pot], 'haemoglobin':[hemo], 'packed_cell_volume':[pcv], 'white_blood_cell_count':[wc], 'red_blood_cell_count':[rc], 'hypertension':[htn], 'diabetes_mellitus':[dm], 'coronary_artery_disease':[cad],
       'appetite':[appet], 'peda_edema':[pe], 'aanemia':[ane],'eGFR':[eGFR]}
        
        input_df=pd.DataFrame(d)
        # Preprocess the input values
        for column in cat_cols:
            input_df[column] = input_df[column].astype(str)  # Ensure values are strings
            le = loaded_label_encoders[column]
            input_df[column] = le.transform(input_df[column])
        input_df_scaled = loaded_scaler.transform(input_df)
        score = model.predict(input_df_scaled)
        return render(request, 'spamreport.html', {"object": score})

    return render(request, 'spaminput.html')
        
def adddata(request):

    return render(request,'spaminput.html')








