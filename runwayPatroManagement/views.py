from django.shortcuts import render
import datetime
from .models import *
from main.models import runway_baseData
from evaluationManagement.models import parameterTab

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
    for type in patrolTypeData:
        for item in patroData:
            if item.patroCount==type['code']:
                type['code'] = 'false'
    context={
        'patroDate':patroDate,
        'allrunways':allrunways,
        'patrolTypeData':patrolTypeData,
        'tzPatroCount':tzPatroCount
    }
    return render(request, 'runwaysPatroManagement/runways/addPatrol_Dialog.html',context)

def patrolTypeDic():
    patrolType = parameterTab.objects.filter(parameterType='patrolType')
    patrolTypeData = []
    for item in patrolType:
        dict = {'code':item.parameterCode,'name':item.parameterName,'flag':'true'}
        patrolTypeData.append(dict)
    return patrolTypeData