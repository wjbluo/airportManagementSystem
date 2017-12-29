from django.shortcuts import render
import datetime
from .models import *
from main.models import runway_baseData
from evaluationManagement.models import parameterTab

# Create your views here.

def showPatrolRecord(request):

    return render(request, 'runwaysPatroManagement/runways/runwayPatroRecord.html')


def addPatrolRecord(request):
    patroDate = datetime.datetime.now().strftime("%Y%m%d")
    allrunways = runway_baseData.objects.all()
    patrolType = parameterTab.objects.filter(parameterType='patrolType')
    runwaysPatroData.objects.filter()
    context={
        'patroDate':patroDate,
        'allrunways':allrunways,
        'patrolType':patrolType
    }
    return render(request, 'runwaysPatroManagement/runways/addPatrol_Dialog.html',context)