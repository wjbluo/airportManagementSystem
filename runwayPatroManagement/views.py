from django.shortcuts import render
import datetime
from .models import *
from main.models import runway_baseData,roleTab,user_roleTab
from evaluationManagement.models import parameterTab
from django.contrib.auth.models import User

# Create your views here.

def showPatrolRecord(request):
    currentDate = datetime.datetime.now().strftime("%Y%m%d")
    context={
        'currentDate':currentDate
    }
    return render(request, 'runwaysPatroManagement/runways/runwayPatroRecord.html',context)


def addPatrolRecord(request):
    patroDate = datetime.datetime.now().strftime("%Y%m%d")
    allrunways = runway_baseData.objects.all()
    patrolType = parameterTab.objects.filter(parameterType='patrolType')
    patroData = runwaysPatroData.objects.filter(patroDate__contains=patroDate)
    tzPatroCount = patroData.filter(patroCount='05').count()+1
    patrolTypeData = patrolTypeDic()
    # 巡视人员
    patrolUserIds= user_roleTab.objects.filter(role__roleName__contains='巡视')
    # role = User .objects.filter(ro)
    for type in patrolTypeData:
        for item in patroData:
            if item.patroCount==type['code']:
                type['code'] = 'false'
    context={
        'patroDate':patroDate,
        'allrunways':allrunways,
        'patrolTypeData':patrolTypeData,
        'tzPatroCount':tzPatroCount,
        'patrolUserIds':patrolUserIds
    }
    return render(request, 'runwaysPatroManagement/runways/addPatrol_Dialog.html',context)

def patrolTypeDic():
    patrolType = parameterTab.objects.filter(parameterType='patrolType')
    patrolTypeData = []
    for item in patrolType:
        dict = {'code':item.parameterCode,'name':item.parameterName,'flag':'true'}
        patrolTypeData.append(dict)
    return patrolTypeData