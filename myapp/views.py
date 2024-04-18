from django.shortcuts import render
from django.http import HttpResponse
from collections import defaultdict
from .models import *
from .forms import *
#from io import TextIOWrapper
from django.contrib import messages
from django_pandas.io import read_frame
import warnings
warnings.filterwarnings(action='once')
import os
import numpy as np
import pandas as pd
#import random
#import cv2
#import tensorflow as tf
#from keras.models import load_model
#from collections import deque
#from moviepy.editor import VideoFileClip
#from keras.preprocessing import image
import pickle
# Create your views here.
#model = joblib.load('model/DT.joblib')
filename = 'model/dt_model.sav'
model = pickle.load(open(filename, 'rb'))

file_path = 'model/scaler.pkl'
with open(file_path , 'rb') as f:
    loaded_scaler = pickle.load(f)


columns=['age', 'blood_pressure', 'specific_gravity', 'albumin', 'sugar',
       'red_blood_cells', 'pus_cell', 'pus_cell_clumps', 'bacteria',
       'blood_glucose_random', 'blood_urea', 'serum_creatinine', 'sodium',
       'potassium', 'haemoglobin', 'packed_cell_volume',
       'white_blood_cell_count', 'red_blood_cell_count', 'hypertension',
       'diabetes_mellitus', 'coronary_artery_disease', 'appetite',
       'peda_edema', 'aanemia','eGFR']

cat_cols = ['red_blood_cells', 'pus_cell', 'pus_cell_clumps', 'bacteria', 'hypertension', 'diabetes_mellitus', 'coronary_artery_disease', 'appetite', 'peda_edema', 'aanemia']



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

def contact(request):
    return render(request,'contact.html')   

def initial_stage(request):
    return render(request, 'initialstage.html')

def first_stage(request):
    return render(request, 'firststage.html')

def second_stage(request):
    return render(request, 'secondstage.html')

def third_stage(request):
    return render(request, 'thirdstage.html')

def fourth_stage(request):
    return render(request, 'fourthstage.html')

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
            print(check)
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
def calculate_egfr(row):
    creatinine = row['serum_creatinine']
    age = row['age']
    systolic_bp = row['blood_pressure']
    
    if pd.notna(creatinine) and pd.notna(age) and pd.notna(systolic_bp):
        return 175 * ((creatinine ** -1.154) * (age ** -0.203) / systolic_bp) * 0.742*100
    else:
        return None

def recommend_output(stage):
    if stage == 1:
        k = ['Early Kidney Damage',
        'CKD Stage 1 indicates very early kidney damage with normal or high filtration rate and usually no symptoms.',
        'Regular screening for those at risk (e.g., diabetes, hypertension) to detect subtle signs or risk factors.',
        'Management focuses on underlying conditions, like hypertension or diabetes, to slow progression.',
        'Maintain a balanced diet low in sodium and processed foods; consult a dietitian for personalized advice.',
        'Regular, moderate-intensity exercise like walking, swimming, or cycling.',
        'Adequate hydration based on individual needs, avoiding overhydration.',
        'Gentle poses like Sukhasana (Easy Pose) for stress management and circulation improvement.']
        return k
        
    elif stage == 2:
        k = ['Mild CKD',
             'CKD Stage 2 is characterized by mild kidney damage with a slight decline in kidney function and often no clear symptoms.',
             'Diagnosis through blood and urine tests showing kidney damage markers; monitoring progression is crucial.',
             'Focus remains on controlling underlying conditions; ACE inhibitors or ARBs may be prescribed to protect kidney function.',
             'Potassium and phosphorus intake may still be normal, but continue a healthy, balanced diet and monitor protein intake.',
             'Continue moderate exercise, incorporating resistance training to maintain muscle strength.',
             'Continue with individual hydration needs, being cautious not to overhydrate.',
             'Including Vajrasana (Thunderbolt Pose) for digestive health and Utkatasana (Chair Pose) for strength.']
        return k

    elif stage == 3:
        k = ['Moderate CKD',
             'CKD Stage 3 involves moderate kidney function decline, with symptoms like fatigue, swelling, and changes in urination becoming more noticeable.',
             'Comprehensive evaluation with blood, urine tests, and imaging; monitoring of kidney function decline rate is essential.',
             'Medications may include those to lower blood pressure, manage anemia, and adjust mineral and bone disorder treatments.',
             'A diet low in phosphorus and potassium becomes important; sodium and protein intake should be monitored.',
             'Exercise should be adjusted based on energy levels and complications; low-impact activities are recommended.',
             'Fluid intake might need adjustments based on swelling and urine output.',
             'Gentle poses like Setu Bandhasana (Bridge Pose) and Bhujangasana (Cobra Pose) for gentle stretching and strengthening.']
        return k  
    elif stage == 4:
        k = ['Severe CKD',
             'CKD Stage 4 shows severe reduction in kidney function, leading to significant accumulation of fluids and waste products in the body.',
             'Regular, detailed assessments to plan for potential kidney replacement therapy (dialysis or transplant).',
             'Comprehensive treatment including erythropoiesis-stimulating agents for anemia and medications to manage other complications.',
             ' Strict dietary restrictions to manage potassium, phosphorus, fluids, and protein intake; often requires the guidance of a dietitian.',
             'Physical activity tailored to individual capability, focusing on gentle, non-strenuous exercises.',
             'Fluid intake strictly monitored to prevent fluid overload, considering urine output and swelling.',
             'Restorative poses like Savasana (Corpse Pose) with support for relaxation and stress reduction, ensuring no strain on the body.']
        return k  
    elif stage == 0:
        k = ['Maintaining Kidney Health',
             ' Individuals without CKD have normal kidney function with no signs of kidney damage. Maintaining this status involves a healthy lifestyle and regular monitoring for those at risk of kidney diseases.',
             'Not required for healthy individuals, but regular check-ups can help ensure kidneys are functioning properly, especially for those with risk factors like diabetes or hypertension.',
             'No specific drugs are needed for healthy kidneys, but maintaining overall health through managing blood pressure and blood sugar levels is key.',
             'A balanced diet rich in fruits, vegetables, whole grains, and low in processed foods and sodium helps maintain kidney health.',
             'Regular physical activity, such as 150 minutes of moderate-intensity aerobic exercise per week, supports overall health and kidney function.',
             'Drink sufficient water to stay hydrated, typically about 2-3 liters per day, depending on individual needs, climate, and activity level.',
             'General wellness yoga poses such as Tadasana (Mountain Pose) for posture and circulation, and Padahastasana (Standing Forward Bend) for relaxation and kidney stimulation.']
        return k      

def checkspam(request):
    if request.method == 'POST':
        age = float(request.POST.get('age'))
        bp = float(request.POST.get('bp'))
        sg = float(request.POST.get('sg'))
        al = float(request.POST.get('al'))
        su = float(request.POST.get('su'))
        rbc = request.POST.get('rbc')
        pc = request.POST.get('pc')
        pcc = request.POST.get('pcc')
        ba = request.POST.get('ba')
        bgr = int(request.POST.get('bgr'))
        bu = int(request.POST.get('bu'))
        sc = int(request.POST.get('sc'))
        sod = int(request.POST.get('sod'))
        pot = int(request.POST.get('pot'))
        hemo = int(request.POST.get('hemo'))
        pcv = int(request.POST.get('pcv'))
        wc = int(request.POST.get('wc'))
        rc = int(request.POST.get('rc'))
        htn = request.POST.get('htn')
        dm = request.POST.get('dm')
        cad = request.POST.get('cad')
        appet = request.POST.get('appet')
        pe = request.POST.get('pe')
        ane = request.POST.get('ane')
        eGFR = float(request.POST.get('eGFR'))
    
        d = {'age':[age], 'blood_pressure':[bp], 'specific_gravity':[sg], 'albumin':[al], 'sugar':[su], 'red_blood_cells':[rbc], 'pus_cell':[pc], 'pus_cell_clumps':[pcc], 'bacteria':[ba], 'blood_glucose_random':[bgr],
    'blood_urea':[bu], 'serum_creatinine':[sc], 'sodium':[sod], 'potassium':[pot], 'haemoglobin':[hemo], 'packed_cell_volume':[pcv], 'white_blood_cell_count':[wc], 'red_blood_cell_count':[rc], 'hypertension':[htn], 'diabetes_mellitus':[dm], 'coronary_artery_disease':[cad],
    'appetite':[appet], 'peda_edema':[pe], 'aanemia':[ane],'eGFR':[eGFR]}
        d
        input_values = pd.DataFrame(d)
        red_blood_cells_mapping = {'abnormal': 0, 'normal': 1}
        pus_cell_mapping = {'abnormal': 0, 'normal': 1}
        pus_cell_clumps_mapping = {'notpresent': 0, 'present': 1}
        bacteria_mapping = {'notpresent': 0, 'present': 1}
        hypertension_mapping = {'no': 0, 'yes': 1}
        diabetes_mellitus_mapping = {'no': 0, 'yes': 1}
        coronary_artery_disease_mapping = {'no': 0, 'yes': 1}
        appetite_mapping = {'good': 0, 'poor': 1}
        peda_edema_mapping = {'no': 0, 'yes': 1}
        aanemia_mapping = {'no': 0, 'yes': 1}

        # Apply mapping to input data
        input_values['red_blood_cells'] = input_values['red_blood_cells'].map(red_blood_cells_mapping)
        input_values['pus_cell'] = input_values['pus_cell'].map(pus_cell_mapping)
        input_values['pus_cell_clumps'] = input_values['pus_cell_clumps'].map(pus_cell_clumps_mapping)
        input_values['bacteria'] = input_values['bacteria'].map(bacteria_mapping)
        input_values['hypertension'] = input_values['hypertension'].map(hypertension_mapping)
        input_values['diabetes_mellitus'] = input_values['diabetes_mellitus'].map(diabetes_mellitus_mapping)
        input_values['coronary_artery_disease'] = input_values['coronary_artery_disease'].map(coronary_artery_disease_mapping)
        input_values['appetite'] = input_values['appetite'].map(appetite_mapping)
        input_values['peda_edema'] = input_values['peda_edema'].map(peda_edema_mapping)
        input_values['aanemia'] = input_values['aanemia'].map(aanemia_mapping)

        # Apply eGFR calculation function
        input_values['eGFR'] = input_values.apply(calculate_egfr, axis=1)
 
        input_df_scaled = loaded_scaler.transform(input_values)
        score = model.predict(input_df_scaled)
        recomendation = recommend_output(score[0])
        return render(request, 'spamreport.html', {"object": score[0],"object1": recomendation[0],"object2": recomendation[1],"object3": recomendation[2],"object4": recomendation[3],"object5": recomendation[4],"object6": recomendation[5],"object7": recomendation[6],"object8": recomendation[7]})

    return render(request, 'spaminput.html')

def adddata(request):
    return render(request,'spaminput.html')

def about(request):
    return render(request,'about.html')

def home(request):
    return render(request,'home.html')    

def contact1(request):
    return render(request,'contact1.html')

def aboutproject(request):
    return render(request,'aboutproject.html')

def recommendation(request):
    return render(request,'recommendation.html')