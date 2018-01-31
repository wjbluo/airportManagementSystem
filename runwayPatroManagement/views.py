from django.shortcuts import render,HttpResponse
from django.http import StreamingHttpResponse
import datetime,time
from .models import *
from main.models import runway_baseData,roleTab,user_roleTab,permissionTab,role_permissionTab
from evaluationManagement.models import parameterTab
import os
from django.conf import settings
import json
from utils import commUtil
from django.contrib.auth.models import User
import pdfkit

# Create your views here.

def showPatrolRecord(request):
    currentDate = datetime.datetime.now().strftime("%Y%m%d")

    patrolDate = {}
    allpatrol = runwaysPatroData.objects.filter(taskType='ph')
    for item in allpatrol:
        nowTime = datetime.datetime.strptime(item.patroDate, "%Y%m%d").strftime("%Y-%m-%d")
        patrolDate.setdefault(nowTime,'')

    # 获取角色权限数量
    count = getPanentCount(request)
    context={
        'currentDate':currentDate,
        'count':count,
        'patrolDate':patrolDate
    }
    return render(request, 'runwaysPatroManagement/runways/runwayPatroRecord.html',context)

def searchPatrolData(request):
    ret = {"code": 0, "msg": "", "count": None, "data": None}
    if request.method == 'POST':
        limit = request.POST['limit']
        page = request.POST['page']
        searchStr = request.POST.get('searchStr', '')
        if searchStr=='':
            nowDate = datetime.datetime.now().strftime("%Y%m%d")
            [startDate, endDate] = [nowDate,nowDate]
        else:
            [startDate,endDate] = searchStr.split(' ~ ',1)
        PatrolData = runwaysPatroData.objects.filter(patroDate__gte=startDate,patroDate__lte=endDate,taskType='ph')

        status = ''
        data = []
        for ls in PatrolData:
            mainCarPerson_list = ls.mainCarPerson.split(';')
            mainCarPerson_str = ''
            for item in mainCarPerson_list:
                if item != '':
                    this_User = User.objects.get(id=int(item))
                    if this_User:
                        mainCarPerson_str+=this_User.first_name+this_User.last_name+';'
            damagesCount = runwaysDamageData.objects.filter(Patro=ls).count()
            mainCarStr = "[主:"+ls.mainCarDirection+"]" if ls.patroMainCar !='' else ''
            SideCarStr = "[副:"+ls.sideCarDirection+"]" if ls.sideCar !='' else ''
            item = {"taskNo": ls.taskNo, "abnormal":"<span style='display:none;' id='taskNo'>"+ls.taskNo+"</span><span style='display:none;'>"+str(damagesCount)+"</span><a style='cursor:pointer;padding-left:5px;' class='iconfont' name='abnormal'>&#xe67d;<span class='layui-badge layui-bg-gray'>"+str(damagesCount)+"</span></a>"
                    , "runwaysCode":runway_baseData.objects.get(id=ls.runways_id).runwayCode,
                    "patroCount": parameterTab.objects.get(parameterType='patrolType',parameterCode=ls.patroCount).parameterName+'<'+ls.patrolReason+'>' if ls.patroCount=='05' else parameterTab.objects.get(parameterType='patrolType',parameterCode=ls.patroCount).parameterName,
                    "direction": mainCarStr+SideCarStr
                    , "notifiedTowerTime": ls.notifiedTowerTime, "entryTime": ls.entryTime,
                    "exitTime": ls.exitTime, "patroMainCar": ls.patroMainCar, "mainCarPerson": mainCarPerson_str,
                    "noPatroReason": ls.noPatroReason if ls.noPatroReason!='' else '/' }
            data.append(item)
        count = PatrolData.__len__()
        [currentpage, maxpage, minpage, maxpage] = commUtil.GetYeMa(page, limit, count)
        ret['count'] = count
        ret['data'] = data[minpage - 1:maxpage]
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'runwaysPatroManagement/runways/runwayPatroRecord.html')

def printStandBook(request,taskNo):
    context={
        'taskNo':taskNo
    }
    return render(request, 'runwaysPatroManagement/apron/printStandBook.html',context)

def standBook(request,taskNo):
    currentTask = runwaysPatroData.objects.get(taskNo=taskNo)
    currentDamage = runwaysDamageData.objects.filter(Patro=currentTask)
    picstr = []
    for item in currentDamage:
        damagePic_list = item.damagePic.split(';')
        for dir in damagePic_list:
            if dir!='':
                picstr.append(dir)
    context = {
        'currentTask':currentTask,
        'currentDamage':currentDamage,
        'picstr':picstr
    }
    return render(request, 'runwaysPatroManagement/apron/standBook.html',context)

def savaAspdf_xsBook(request,taskNo,posi):
    # config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files (x86)\\wkhtmltopdf\\bin\\wkhtmltopdf.exe',)
    if posi=='jp':
        pdfkit.from_url(request.get_host() + '/component/runwayPatroManagement/showApronRecord/printStandBook/'+taskNo+'/standBook/', 'upload/lsDir/jp.pdf')
        filename = 'jp'
        filepath = 'upload/lsDir/jp.pdf'
    if posi=='ph':
        pdfkit.from_url(request.get_host() + '/component/runwayPatroManagement/showPatrolRecord/printStandBook/'+taskNo+'/standBook/', 'upload/lsDir/ph.pdf')
        filename = 'ph'
        filepath = 'upload/lsDir/ph.pdf'

    def file_iterator(file_name):
        with open(file_name,'rb') as f:
            while True:
                c = f.read()
                if c:
                    yield c
                else:
                    break


    response = StreamingHttpResponse(file_iterator(filepath))
    response['Content-Type'] = 'application/octet-stream'
    agent = request.META.get('HTTP_USER_AGENT')
    if agent.upper().find("MSIE") != -1:
        response['Content-Disposition'] ="attachment; filename={0}".format(filename + '.pdf').encode('gbk').decode('latin-1')
    elif agent.upper().find("EDGE") != -1:
        response['Content-Disposition'] = "attachment; filename={0}".format(filename+'.pdf').encode('gb2312')
    else:
        response['Content-Disposition'] = "attachment; filename={0}".format(filename + '.pdf').encode('utf8')
    return response

def getPanentCount(request):
    user = request.user
    roles = roleTab.objects.filter(user_roletab__user=user)
    role_permission = role_permissionTab.objects.filter(role__in=roles)
    owner_permiss = []
    for item in role_permission:
        owner_permiss.append(item.persission.menuId)
    count = permissionTab.objects.filter(parentmenuId='0',menuId__in=owner_permiss).count()
    return count

def addPatrolRecord(request):
    patroDate = datetime.datetime.now().strftime("%Y%m%d")
    allrunways = runway_baseData.objects.all()
    patrolType = parameterTab.objects.filter(parameterType='patrolType',extra__contains='跑滑巡视')
    patroData = runwaysPatroData.objects.filter(patroDate__contains=patroDate,taskType='ph')
    tzPatroCount = patroData.filter(patroCount='05').count()+1
    patrolTypeData = patrolTypeDic(patrolType)
    # 巡视人员
    patrolUserIds= user_roleTab.objects.filter(role__roleName__contains='巡视')
    # role = User .objects.filter(ro)
    for type in patrolTypeData:
        for item in patroData:
            if item.patroCount==type['code'] and type['code']!='05':
                type['flag'] = 'false'
    count = getPanentCount(request)
    runwaysDamageData_ls.objects.all().delete()
    context={
        'patroDate':patroDate,
        'allrunways':allrunways,
        'patrolTypeData':patrolTypeData,
        'tzPatroCount':tzPatroCount,
        'patrolUserIds':patrolUserIds,
        'count':count
    }
    return render(request, 'runwaysPatroManagement/runways/addPatrol_Dialog.html',context)

def patrolTypeDic(patrolType):
    # patrolType = parameterTab.objects.filter(parameterType='patrolType',extra__contains='跑滑巡视')
    patrolTypeData = []
    for item in patrolType:
        dict = {'code':item.parameterCode,'name':item.parameterName,'flag':'true'}
        patrolTypeData.append(dict)
    return patrolTypeData

def addDamageRecord(request):
    patrolDamgeTypes = parameterTab.objects.filter(parameterType='patrolDam')
    groups = patrolDamgeTypes.values('extra').distinct()
    context={
        'patrolDamgeTypes':patrolDamgeTypes,
        'groups':groups
    }
    return render(request, 'runwaysPatroManagement/runways/addDamage_Dialog.html',context)


def receiveRadio(request):
    ret = {"code": 0, "msg": "", "count": None, "path": None}
    if request.method=='POST':
        reqfile = request.FILES.get("file")
        filename = reqfile.name

        current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        pathdir = os.path.join(settings.MEDIA_ROOT, 'patrolRadio',current_time).replace('\\', '/')
        pathRela = os.path.join('patrolRadio',current_time,filename).replace('\\','/')
        dest = os.path.join(settings.MEDIA_ROOT, 'patrolRadio',current_time,filename).replace('\\', '/')

        if not os.path.exists(pathdir):
            os.makedirs(pathdir)

        try:
            with open(dest, "wb") as destination:
                for chunk in reqfile.chunks():
                    destination.write(chunk)
            ret['path'] = pathRela
        except  Exception as e:
            ret['code'] = 1
            ret['msg'] = '传输错误'
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'runwaysPatroManagement/runways/addPatrol_Dialog.html')

def receiveDamagePic(request):
    ret = {"code": 0, "msg": "", "count": None, "path": None}
    if request.method == 'POST':
        reqfile = request.FILES.get("file")
        filename = reqfile.name

        current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        pathdir = os.path.join(settings.MEDIA_ROOT, 'patrolPic', current_time).replace('\\', '/')
        pathRela = os.path.join('patrolPic', current_time, filename).replace('\\', '/')
        dest = os.path.join(settings.MEDIA_ROOT, 'patrolPic', current_time, filename).replace('\\', '/')

        if not os.path.exists(pathdir):
            os.makedirs(pathdir)

        try:
            with open(dest, "wb") as destination:
                for chunk in reqfile.chunks():
                    destination.write(chunk)
            ret['path'] = pathRela
        except  Exception as e:
            ret['code'] = 1
            ret['msg'] = '传输错误'
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'runwaysPatroManagement/runways/addDamage_Dialog.html')

def patrolRecordSubmit(request):
    ret = {'status': False, 'message': '', 'data': None, 'planId': None}
    if request.method == 'POST':
        try:
            post_data = request.POST.get('post_data', None)
            post_data_dict = json.loads(post_data)

            if post_data_dict['patroDate'] == '' or post_data_dict['patrolType'] == '' or len(post_data_dict['patroDate'])!=8:
                ret['message'] = '巡视日期、巡视类型必填且日期需符合日期格式。'
            else:
                # patrolRunways = runway_baseData.objects.get(id=post_data_dict['runwaysCode'])
                mainCarPerson = ''
                sideCarPerson = ''
                tools = ''
                if len(post_data_dict['mainCarPerson'])!=0:
                    mainlist = post_data_dict['mainCarPerson']
                    for user in mainlist:
                        mainCarPerson+=user['val']+';'
                if len(post_data_dict['sideCarPerson']) != 0:
                    sidelist = post_data_dict['sideCarPerson']
                    for user in sidelist:
                        sideCarPerson += user['val'] + ';'
                for tool in post_data_dict['tools_value']:
                    tools+=tool+';'
                runwaysPatroData.objects.create(
                    taskNo=post_data_dict['taskNo'],
                    weather = post_data_dict['weather'],
                    patroDate = post_data_dict['patroDate'],
                    runways_id = post_data_dict['runwaysCode'],
                    patroCount = post_data_dict['patrolType'],
                    patrolReason =  post_data_dict['patrolReason'],
                    patroMainCar = post_data_dict['patroMainCar'],
                    mainCarPerson = mainCarPerson,
                    mainCarDirection = post_data_dict['mainCarDirection'],
                    mainCarTrail = '',
                    sideCar = post_data_dict['sideCar'],
                    sideCarPerson = sideCarPerson,
                    sideCarDirection = post_data_dict['sideCarDirection'],
                    sideCarTrail = '',

                    carryGoods = tools,

                    notifiedTowerTime = post_data_dict['notifiedTowerTime'],
                    notifiedFlyingTime = post_data_dict['notifiedFlyingTime'],

                    entryTime = post_data_dict['entryTime'],
                    exitWaitingTime = '',
                    exitWaitingPosition = '',
                    Re_entryTime = '',

                    exitNotifiedTowerTime = post_data_dict['exitNotifiedTowerTime'],
                    exitNotifiedFlyingTime = post_data_dict['exitNotifiedFlyingTime'],
                    exitTime = post_data_dict['exitTime'],

                    noPatroReason = post_data_dict['noPatroReason'],
                    radioDis = post_data_dict['pathStr'],
                    flag = post_data_dict['choose'],
                    taskType = 'ph'
                )
                runwaysPatroData_now = runwaysPatroData.objects.filter(taskType='ph').first()
                ls_data = runwaysDamageData_ls.objects.all()
                for item in ls_data:
                    pass
                    runwaysDamageData.objects.create(
                        Patro=runwaysPatroData_now,
                        # damageNo = item.id,
                        runwayType = item.runwayType,
                        damageType = item.damageType,
                        partitionCode = item.partitionCode,
                        Row = item.Row,
                        Col = item.Col,
                        X = item.X,
                        Y = item.Y,
                        location = item.location,
                        damageLength = item.damageLength,
                        damageWidth = item.damageWidth,
                        damageArea = item.damageArea,

                        desc = item.desc,
                        damagePic = item.damagePic
                    )
                ret['message'] = '保存成功！'
                ret['status'] = True
        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'runwaysPatroManagement/runways/addPatrol_Dialog.html.html')

def patrolDamageSubmit(request):

    ret = {'status': False, 'message': '', 'data': None, 'planId': None}
    if request.method == 'POST':
        try:
            post_data = request.POST.get('post_data', None)
            post_data_dict = json.loads(post_data)
            # 先清空所有数据
            if post_data_dict['damageType']=='' or post_data_dict['facility']=='':
                ret['message'] = '设施类别和设施异常为必填项。'
            else:
            # runwaysDamageData_ls.objects.all().delete()
                runwaysDamageData_ls.objects.create(
                    runwayType=post_data_dict['facility'],
                    damageType = post_data_dict['damageType'],
                    partitionCode = post_data_dict['cellCode'],
                    Row = post_data_dict['x'],
                    Col = post_data_dict['y'],
                    X = post_data_dict['x'],
                    Y = post_data_dict['y'],
                    location = post_data_dict['position'],
                    damageLength = post_data_dict['damage_length'],
                    damageWidth = post_data_dict['damage_width'],
                    damageArea = post_data_dict['damage_area'],

                    desc = post_data_dict['Dis'],
                    damagePic = post_data_dict['pathStr'],
                )
                ret['message'] = '保存成功！'
                ret['status'] = True
        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'runwaysPatroManagement/runways/addDamage_Dialog.html')

def searchPatrolDamage(request):
    ret = {"code": 0, "msg": "", "count": None, "data": None}
    if request.method=='POST':
        limit = request.POST['limit']
        page = request.POST['page']
        searchStr = request.POST.get('searchStr','')
        DamageData_ls = runwaysDamageData_ls.objects.all()

        status = ''
        data=[]
        for ls in DamageData_ls:
            item = {"id":ls.id,"location": ls.location, "partitionCode": ls.partitionCode,
                    "runwayType": parameterTab.objects.get(parameterType='patrolDam',parameterCode=ls.runwayType).parameterName,
                    "damageType": ls.damageType, "row_col": '('+ls.X+','+ls.Y+')',"row":ls.X,"col":ls.Y,
                    "damageLength": ls.damageLength, "damageWidth": ls.damageWidth,"damageArea":ls.damageArea,"damagePic_dis":ls.damagePic}
            data.append(item)
        count = DamageData_ls.__len__()
        [currentpage, maxpage, minpage, maxpage] = commUtil.GetYeMa(page, limit, count)
        ret['count'] = count
        ret['data'] = data[minpage - 1:maxpage]
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'runwaysPatroManagement/runways/addPatrol_Dialog.html')

def showPatrolDamage(request,taskNo):
    currentTask= runwaysPatroData.objects.get(taskNo=taskNo)
    damagesList =runwaysDamageData.objects.filter(Patro = currentTask)
    context={
        'damagesList':damagesList
    }
    return render(request, 'runwaysPatroManagement/runways/damageSider.html',context)

def showDamage(request,taskNo,damageId):
    currentTask= runwaysPatroData.objects.get(taskNo=taskNo)
    currentDamage = runwaysDamageData.objects.get(damageNo = damageId)
    context = {
        'currentTask':currentTask,
        'currentDamage':currentDamage
    }
    return render(request, 'runwaysPatroManagement/runways/damageDetail.html',context)




# 讥评巡视模块
def showApronRecord(request):
    currentDate = datetime.datetime.now().strftime("%Y%m%d")


    patrolDate = {}
    allpatrol = runwaysPatroData.objects.filter(taskType='jp')
    for item in allpatrol:
        nowTime = datetime.datetime.strptime(item.patroDate, "%Y%m%d").strftime("%Y-%m-%d")
        patrolDate.setdefault(nowTime,'')

    #获取角色权限数量
    count = getPanentCount(request)
    context={
        'currentDate':currentDate,
        'count':count,
        'patrolDate':patrolDate
    }
    return render(request, 'runwaysPatroManagement/apron/apronPatroRecord.html',context)

def searchApronPatrolData(request):
    ret = {"code": 0, "msg": "", "count": None, "data": None}
    if request.method == 'POST':
        limit = request.POST['limit']
        page = request.POST['page']
        searchStr = request.POST.get('searchStr', '')
        if searchStr=='':
            nowDate = datetime.datetime.now().strftime("%Y%m%d")
            [startDate, endDate] = [nowDate,nowDate]
        else:
            [startDate,endDate] = searchStr.split(' ~ ',1)
        PatrolData = runwaysPatroData.objects.filter(patroDate__gte=startDate,patroDate__lte=endDate,taskType='jp')

        status = ''
        data = []
        for ls in PatrolData:
            mainCarPerson_list = ls.mainCarPerson.split(';')
            mainCarPerson_str = ''
            for item in mainCarPerson_list:
                if item != '':
                    this_User = User.objects.get(id=int(item))
                    if this_User:
                        mainCarPerson_str+=this_User.first_name+this_User.last_name+';'
            damagesCount = runwaysDamageData.objects.filter(Patro=ls).count()
            mainCarStr = "[主:"+ls.mainCarDirection+"]" if ls.patroMainCar !='' else ''
            # SideCarStr = "[副:"+ls.sideCarDirection+"]" if ls.sideCar !='' else ''
            item = {"taskNo": ls.taskNo, "abnormal":"<span style='display:none;' id='taskNo'>"+ls.taskNo+"</span><span style='display:none;'>"+str(damagesCount)+"</span><a style='cursor:pointer;padding-left:5px;' class='iconfont' name='abnormal'>&#xe67d;<span class='layui-badge layui-bg-gray'>"+str(damagesCount)+"</span></a>"
                    ,"patroCount": parameterTab.objects.get(parameterType='patrolType',parameterCode=ls.patroCount).parameterName+'<'+ls.patrolReason+'>' if ls.patroCount=='05' else parameterTab.objects.get(parameterType='patrolType',parameterCode=ls.patroCount).parameterName,
                     "entryTime": ls.entryTime,
                    "exitTime": ls.exitTime, "patroMainCar": ls.patroMainCar, "mainCarPerson": mainCarPerson_str}
            data.append(item)
        count = PatrolData.__len__()
        [currentpage, maxpage, minpage, maxpage] = commUtil.GetYeMa(page, limit, count)
        ret['count'] = count
        ret['data'] = data[minpage - 1:maxpage]
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'runwaysPatroManagement/apron/apronPatroRecord.html')

def addApronPatrolRecord(request):
    patroDate = datetime.datetime.now().strftime("%Y%m%d")
    allrunways = runway_baseData.objects.all()
    patrolType = parameterTab.objects.filter(parameterType='patrolType',extra__contains='机坪巡视')
    patroData = runwaysPatroData.objects.filter(patroDate__contains=patroDate,taskType='jp')
    tzPatroCount = patroData.filter(patroCount='05').count()+1
    patrolTypeData = patrolTypeDic(patrolType)
    # 巡视人员
    patrolUserIds= user_roleTab.objects.filter(role__roleName__contains='巡视')
    # role = User .objects.filter(ro)
    for type in patrolTypeData:
        for item in patroData:
            if item.patroCount==type['code'] and type['code']!='05':
                type['flag'] = 'false'
    count = getPanentCount(request)
    runwaysDamageData_ls.objects.all().delete()
    context={
        'patroDate':patroDate,
        'allrunways':allrunways,
        'patrolTypeData':patrolTypeData,
        'tzPatroCount':tzPatroCount,
        'patrolUserIds':patrolUserIds,
        'count':count
    }
    return render(request, 'runwaysPatroManagement/apron/addApronPatrol_Dialog.html',context)

def addDamageRecord_apron(request):
    patrolDamgeTypes = parameterTab.objects.filter(parameterType='patrolDam')
    groups = patrolDamgeTypes.values('extra').distinct()
    context={
        'patrolDamgeTypes':patrolDamgeTypes,
        'groups':groups
    }
    return render(request, 'runwaysPatroManagement/apron/addDamage_Dialog.html',context)

def patrolDamageSubmit_apron(request):

    ret = {'status': False, 'message': '', 'data': None, 'planId': None}
    if request.method == 'POST':
        try:
            post_data = request.POST.get('post_data', None)
            post_data_dict = json.loads(post_data)
            # 先清空所有数据
            if post_data_dict['damageType']=='' or post_data_dict['facility']=='':
                ret['message'] = '设施类别和设施异常为必填项。'
            else:
            # runwaysDamageData_ls.objects.all().delete()
                runwaysDamageData_ls.objects.create(
                    runwayType=post_data_dict['facility'],
                    damageType = post_data_dict['damageType'],
                    partitionCode = post_data_dict['cellCode'],
                    Row = post_data_dict['x'],
                    Col = post_data_dict['y'],
                    X = post_data_dict['x'],
                    Y = post_data_dict['y'],
                    location = post_data_dict['position'],
                    damageLength = post_data_dict['damage_length'],
                    damageWidth = post_data_dict['damage_width'],
                    damageArea = post_data_dict['damage_area'],

                    desc = post_data_dict['Dis'],
                    damagePic = post_data_dict['pathStr'],
                )
                ret['message'] = '保存成功！'
                ret['status'] = True
        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'runwaysPatroManagement/apron/addDamage_Dialog.html')

def patrolRecordSubmit_apron(request):
    ret = {'status': False, 'message': '', 'data': None, 'planId': None}
    if request.method == 'POST':
        try:
            post_data = request.POST.get('post_data', None)
            post_data_dict = json.loads(post_data)

            if post_data_dict['patroDate'] == '' or post_data_dict['patrolType'] == '' or len(post_data_dict['patroDate'])!=8:
                ret['message'] = '巡视日期、巡视类型必填且日期需符合日期格式。'
            else:
                mainCarPerson = ''
                tools = ''
                if len(post_data_dict['mainCarPerson'])!=0:
                    mainlist = post_data_dict['mainCarPerson']
                    for user in mainlist:
                        mainCarPerson+=user['val']+';'
                for tool in post_data_dict['tools_value']:
                    tools+=tool+';'
                runwaysPatroData.objects.create(
                    taskNo=post_data_dict['taskNo'],
                    weather = post_data_dict['weather'],
                    patroDate = post_data_dict['patroDate'],
                    patroCount = post_data_dict['patrolType'],
                    patrolReason =  post_data_dict['patrolReason'],
                    patroMainCar = post_data_dict['patroMainCar'],
                    mainCarPerson = mainCarPerson,
                    mainCarDirection = '',
                    mainCarTrail = '',
                    sideCar = '',
                    sideCarPerson = '',
                    sideCarDirection = '',
                    sideCarTrail = '',

                    carryGoods = tools,

                    notifiedTowerTime = '',
                    notifiedFlyingTime = '',

                    entryTime = post_data_dict['entryTime'],
                    exitWaitingTime = '',
                    exitWaitingPosition = '',
                    Re_entryTime = '',

                    exitNotifiedTowerTime = '',
                    exitNotifiedFlyingTime = '',
                    exitTime = post_data_dict['exitTime'],

                    noPatroReason = '',
                    radioDis = post_data_dict['pathStr'],
                    flag = post_data_dict['choose'],
                    taskType = 'jp'
                )
                runwaysPatroData_now = runwaysPatroData.objects.filter(taskType='jp').first()
                ls_data = runwaysDamageData_ls.objects.all()
                for item in ls_data:
                    pass
                    runwaysDamageData.objects.create(
                        Patro=runwaysPatroData_now,
                        # damageNo = item.id,
                        runwayType = item.runwayType,
                        damageType = item.damageType,
                        partitionCode = item.partitionCode,
                        Row = item.Row,
                        Col = item.Col,
                        X = item.X,
                        Y = item.Y,
                        location = item.location,
                        damageLength = item.damageLength,
                        damageWidth = item.damageWidth,
                        damageArea = item.damageArea,

                        desc = item.desc,
                        damagePic = item.damagePic
                    )
                ret['message'] = '保存成功！'
                ret['status'] = True
        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'runwaysPatroManagement/runways/addPatrol_Dialog.html.html')