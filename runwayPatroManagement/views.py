from django.shortcuts import render

# Create your views here.

def showPatrolRecord(request):

    return render(request, 'runwaysPatroManagement/runways/runwayPatroRecord.html')


def addPatrolRecord(request):
    return render(request, 'runwaysPatroManagement/runways/runwayPatroRecord.html')