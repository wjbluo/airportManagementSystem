from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from .models import *
from django.contrib.auth.decorators import login_required
import json,math
from django.contrib.auth.models import User
from django.contrib import auth
import string
from django.db import connections
import time
from django.forms.models import model_to_dict
from django.db import transaction
from utils import commUtil
from django.db.models import Sum,Count
# Create your views here.



# def GetYeMa(page,limit,count):
#     page = int(page)
#     limit = int(limit)
#     maxPage = math.ceil(count/limit)
#     if int(page)<=1:
#         return 1,maxPage,1,limit
#     if int(page)>maxPage:
#         return maxPage,maxPage,(maxPage-1)*limit+1,maxPage*limit
#     return int(page),maxPage,(int(page)-1)*limit+1, int(page)*limit

@login_required(login_url='/account/login/')
def index(request):
    if request.COOKIES.get('currentAirportId'):
        username = request.user.username
        SystemMenu = GetSystemMenu(request.user)
        context={
            'username':username,
            'SystemMenu':SystemMenu
        }
        return render(request, 'main.html',context)
    else:
        auth.logout(request)
        response = HttpResponseRedirect('/account/login/')
        return response


def GetSystemMenu(user):
    this_user_roles = user_roleTab.objects.filter(user=user)
    owner_per =  permissionTab.objects.filter(menuId='x')
    if this_user_roles:
        for role in this_user_roles:
            role_tab = roleTab.objects.get(id=role.role_id)
            role_per = role_permissionTab.objects.filter(role=role_tab)
            for ls_per in role_per:
                per = permissionTab.objects.filter(id=ls_per.persission.id).order_by('level')
                owner_per=owner_per|per
    menuData = owner_per.filter(parentmenuId='0')
    menu = []
    for item1 in menuData:
        topMenu = { 'title':item1.menuTitle,'icon':item1.icon,'isCurrent':'true' if item1.isCurrent=='1' else '','href':item1.url,'menu':None}
        firstMenu = owner_per.filter(parentmenuId=item1.menuId)
        firstMenu_all = []
        if firstMenu:

            for item2 in firstMenu:
                firstMenu_ = {'title': item2.menuTitle, 'icon': item2.icon,
                                    'isCurrent': 'true' if item2.isCurrent == '1' else 'false', 'href': item2.url,
                                    'children': None}
                secondMenu = owner_per.filter(parentmenuId=item2.menuId)
                secondMenu_all = []
                if secondMenu:

                    for item3 in secondMenu:
                        secondMenu_ = {'title': item3.menuTitle, 'icon': item3.icon,
                                      'isCurrent': 'true' if item3.isCurrent == '1' else 'false', 'href': item3.url,
                                      'children': None}
                        thirdMenu= owner_per.filter(parentmenuId=item3.menuId)
                        thirdMenu_all = []
                        if thirdMenu:

                            for item4 in thirdMenu:
                                thirdMenu_ = {'title': item4.menuTitle, 'icon': item4.icon,
                                               'isCurrent': 'true' if item4.isCurrent == '1' else 'false',
                                               'href': item4.url,
                                               'children': []}
                                thirdMenu_all.append(thirdMenu_)
                        else:
                            secondMenu_['children']=[]
                        secondMenu_['children'] = thirdMenu_all
                        secondMenu_all.append(secondMenu_)
                else:
                    firstMenu_['children']=[]
                # firstMenu_all.append(firstMenu_)
                firstMenu_['children'] = secondMenu_all
                firstMenu_all.append(firstMenu_)
            topMenu['menu']=firstMenu_all
        else:
            topMenu['menu']=[{}]
        menu.append(topMenu)
    return menu


# userManag 用户管理
def userManag(request):
    return render(request, 'authorization/userManage.html')

def addUser(request):
    return render(request, 'authorization/addUserDialog.html')

def addUserSubmit(request):
    ret = {'status': False, 'message': '', 'data': None}
    if request.method == 'POST':
        try:
            post_data = request.POST.get('post_data', None)
            post_data_dict = json.loads(post_data)

            username = post_data_dict['username']
            firstname =  post_data_dict['firstname']
            lastname = post_data_dict['lastname']
            psd = post_data_dict['psd']
            email = post_data_dict['email']

            user = auth.authenticate(username=username, password=psd)
            if user is not None:
                ret['message'] = '该账户已存在。'
            else:
                newUser = User()
                newUser.username = username
                newUser.set_password(psd)
                newUser.email = email
                newUser.first_name = firstname
                newUser.last_name = lastname
                newUser.save()
                ret['message'] = '添加员工信息成功。'
                ret['status'] = True
        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'authorization/addUserDialog.html')

def searchUser(request):
    ret = {"code": 0, "msg": "", "count": None, "data": None}
    if request.method=='POST':
        limit = request.POST['limit']
        page = request.POST['page']
        searchStr = request.POST.get('searchStr','')
        users = User.objects.filter(username__contains=searchStr)

        status = ''
        data=[]
        for user in users:
            if user.is_active == 1:
                status = '正常'
            else:
                status = '已冻结'
            thisUser_role = user_roleTab.objects.filter(user=user)
            roleStr = ""
            for item in thisUser_role:
                roleStr+=item.role.roleName+"、"
            item = {"id": user.id, "username": user.username, "name": user.first_name + user.last_name,
                    "email": user.email, "date_joined": str(user.date_joined), "last_login": str(user.last_login),
                    "roleStr": roleStr, "status": status}
            data.append(item)
        count = users.__len__()
        [currentpage, maxpage, minpage, maxpage] = commUtil.GetYeMa(page, limit, count)
        ret['count'] = count
        ret['data'] = data[minpage - 1:maxpage]
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'authorization/userManage.html')

def frozen(request):
    ret = {"code": 0, "msg": ""}
    if request.method == 'POST':
        post_data = request.POST.get('post_data', None)
        post_data_dict = json.loads(post_data)

        id = post_data_dict['id']
        user = User.objects.get(id=id)

        if user.is_active:
            User.objects.filter(id=id).update(is_active=0)
            ret['msg'] = '账户['+user.username+']已被冻结。'
        else:
            User.objects.filter(id=id).update(is_active=1)
            ret['msg'] = '账户[' + user.username + ']已被解冻。'
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'authorization/userManage.html')

def giveRole(request,userId):
    roles = roleTab.objects.all();
    currentUser = User.objects.get(id=userId)
    currentUserRole = user_roleTab.objects.filter(user = currentUser)
    data = []
    checkedData = []
    currentUserRoleId = []
    for userrole  in  currentUserRole:
        currentUserRoleId.append(userrole.role.id)
    for item in roles:
            if item.id in currentUserRoleId:
                data.append(
                    {"id": item.id, "pId": 0, "name": item.roleName, "value": item.roleDis, "open": "false",
                     "checked": 'true'})
                checkedData.append({"id":item.id,"roleName":item.roleName,"roleDis":item.roleDis})
            else:
                data.append({"id": item.id, "pId": 0, "name": item.roleName, "value": item.roleDis, "open": "false"})
    context={
        "data":data,
        "userId":userId,
        "checkedData":checkedData
    }
    return render(request, 'authorization/giveRoleDialog.html',context)

def giveRoleSubmit(request):
    ret = {'status': False, "msg": "", "count": None, "data": None}
    if request.method == 'POST':
        try:
            post_data = request.POST.get('post_data', None)
            userId = request.POST.get('userId', None)
            post_data_dict = json.loads(post_data)
            user = User.objects.get(id=userId)
            if userId is not None and len(post_data_dict)!=0:
                user_roleTab.objects.filter(user = user).delete()
                for item in post_data_dict:
                    roleId = item['id']
                    role = roleTab.objects.get(id=roleId)
                    user_roleTab.objects.create(user = user,role = role)
                ret['status'] = True
                ret['msg'] = '设置角色成功！'
        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'authorization/giveRoleDialog.html')

# 角色管理
def roleManag(request):
    return render(request, 'authorization/roleManage.html')

def searchGroup(request):
    ret = {"code": 0, "msg": "", "count": None, "data": None}
    if request.method == 'POST':
        limit = request.POST['limit']
        page = request.POST['page']
        searchStr = request.POST.get('searchStr', '')

        roles = roleTab.objects.filter(roleName__contains=searchStr)

        status = ''
        data = []
        for role in roles:
            item = {"id": role.id, "roleName": role.roleName, "roleDis": role.roleDis}
            data.append(item)
        count = roles.__len__()
        [currentpage, maxpage, minpage, maxpage] = commUtil.GetYeMa(page, limit, count)
        ret['count'] = count
        ret['data'] = data[minpage - 1:maxpage]
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'authorization/roleManage.html')

def addGroup(request):
    return render(request, 'authorization/addGroupDialog.html')

def addGroupSubmit(request):
    ret = {'status': False, 'message': '', 'data': None}
    if request.method == 'POST':
        try:
            post_data = request.POST.get('post_data', None)
            post_data_dict = json.loads(post_data)

            groupname = post_data_dict['groupname']
            groupDis = post_data_dict['groupDis']

            if groupDis=='' or groupDis=='':
                pass
            else:
                role = roleTab.objects.filter(roleName=groupname)
                if role.__len__()>0:
                    ret['message'] = '该角色已存在。'
                else:
                    roleTab.objects.create(roleName=groupname,roleDis = groupDis)
                    ret['message'] = '添加角色信息成功。'
                    ret['status'] = True
        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'authorization/addGroupDialog.html')

def lookUsers(request,roleId):
    ret = {"code": 0, "msg": "", "count": None, "data": None}
    if request.method=='POST':
        try:
            limit = request.POST['limit']
            page = request.POST['page']
            searchStr = request.POST.get('searchStr', '')
            currentRole = roleTab.objects.filter(id=roleId)
            currentUser_role = user_roleTab.objects.filter(role=currentRole)
            item = []
            status = ''
            for user_role in currentUser_role:
                if user_role.user.is_active == 1:
                    status = '正常'
                else:
                    status = '已冻结'
                if searchStr in user_role.user.username or searchStr in user_role.user.first_name +  user_role.user.last_name or searchStr=='':
                    item.append({"id": user_role.user.id, "username":  user_role.user.username, "name":  user_role.user.first_name +  user_role.user.last_name,"status":status})
            count=item.__len__()
            [currentpage, maxpage, minpage, maxpage] = commUtil.GetYeMa(page, limit, count)
            ret['count'] = count
            ret['data'] = item[minpage - 1:maxpage]
        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    else:
        context={
            'roleId':roleId
        }
    return render(request, 'authorization/lookUserUnderRole.html',context)

def givePermission(request,roleId):
    currentRole = roleTab.objects.get(id=roleId)
    currentRole_permission = role_permissionTab.objects.filter(role=currentRole)
    owner_per = permissionTab.objects.filter(menuId='x')
    for ls_per in currentRole_permission:
        per = permissionTab.objects.filter(id=ls_per.persission.id)
        owner_per = owner_per | per

    all_permisson = permissionTab.objects.all()
    data = []
    for item in all_permisson:
        if item in owner_per:
            data.append(
                {"id": item.menuId, "pId": item.parentmenuId,"id_true":item.id, "name": item.menuTitle, "open": 'true',
                 "checked": 'true'})
        else:
            data.append(
                {"id": item.menuId, "pId": item.parentmenuId,"id_true":item.id, "name": item.menuTitle, "open": 'true',
                 "checked": 'false'})
    context = {
        "data": data,
        "roleId": roleId,
    }
    return render(request, 'authorization/givePermissionDialog.html', context)

def givePermissionSubmit(request,roleId):
    ret = {'status': False, 'message': '', 'data': None}
    currentRole = roleTab.objects.get(id=roleId)
    role_permissionTab.objects.filter(role = currentRole).delete()
    if request.method == 'POST':
        try:
            post_data = request.POST.get('post_data', None)
            post_data_dict = json.loads(post_data)
            for item in post_data_dict:
                currentper = permissionTab.objects.get(id=item['id'])
                role_permissionTab.objects.create(role = currentRole,persission=currentper)
            ret['message'] = '更新权限成功。'
            ret['status']=True
        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'authorization/givePermissionDialog.html')

def initAirportBasicInformation(request):
    #TOOD 暂时针对一个机场  后需改制针对任意机场  由 登录页选择
    currentAirportId = request.COOKIES.get('currentAirportId', None)
    airportBaseData = airport_baseData.objects.get(id=currentAirportId)
    context={
        'airportBaseData':airportBaseData
    }
    return render(request, 'baseData/airportBasicInformation.html',context)

def alterAirportData(request):
    currentAirportId = request.COOKIES.get('currentAirportId', None)
    airportBaseData = airport_baseData.objects.get(id=currentAirportId)
    context={
        'airportBaseData': airportBaseData
    }
    return render(request, 'baseData/alterAirData_Dialog.html', context)

def alterDataSubmit(request):
    ret = {'status': False, 'message': '', 'data': None,'data_name':None}
    if request.method == 'POST':
        try:
            post_data = request.POST.get('post_data', None)
            post_data_dict = json.loads(post_data)
            currentAirportId = request.COOKIES.get('currentAirportId', None)
            currentAirport = airport_baseData.objects.filter(id=currentAirportId)
            if currentAirport:
                currentAirport.update(
                    airportName=post_data_dict['airportName'],
                    airportCode=post_data_dict['airportCode'],
                    manageInstitution=post_data_dict['manageInstitution'],
                    airportLevel=post_data_dict['airportLevel'],
                    runwayNum=int(post_data_dict['runwayNum']),
                    smoothRoadNum=int(post_data_dict['smoothRoadNum']),
                    roadSurfaceArea= float(post_data_dict['roadSurfaceArea']),
                    soilSurfaceArea= float(post_data_dict['soilSurfaceArea']),
                    seatOfPlaneNum = int(post_data_dict['seatOfPlaneNum']),
                    shippingTime=post_data_dict['shippingTime'],
                    recordingTime=post_data_dict['recordingTime'],
                    updateTime=time.strftime( '%Y-%m-%d %X', time.localtime() )
                )
                data_models = airport_baseData.objects.get(id=currentAirportId)
                data =['机场名称',data_models.airportName,
                       '机场编码', data_models.airportCode,
                       '管理机构', data_models.manageInstitution,
                       '机场等级', data_models.airportLevel,
                       '跑道数量', data_models.runwayNum,
                       '平滑道数量', data_models.smoothRoadNum,
                       '道面面积', str(data_models.roadSurfaceArea)+'KM&sup2;',
                       '土面面积', str(data_models.soilSurfaceArea)+'KM&sup2;',
                       '机位数量', data_models.seatOfPlaneNum,
                       '通航时间', data_models.shippingTime,
                       '记录时间', data_models.recordingTime,
                       '更新时间', data_models.updateTime]
                ret['data'] =data
                ret['message'] = '修改机场基本信息成功。'
                ret['status'] = True
        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'baseData/alterAirData_Dialog.html')

def initRunwayBasicInformation(request):
    return render(request, 'baseData/runwayBasicInfomation.html')

def initRunwayiFrame(request):
    haveRunways = runway_baseData.objects.all()
    context={
        'haveRunways':haveRunways
    }
    return render(request, 'baseData/runWayInfo.html',context)

def addRunwayData(request):
    currentAirportId = request.COOKIES.get('currentAirportId', None)
    currentAirport = airport_baseData.objects.get(id=currentAirportId)
    context={
        'currentAirport': currentAirport
    }
    return render(request, 'baseData/addRunway_Dialog.html', context)

def addRunwayDataSubmit(request):
    ret = {'status': False, 'message': '', 'data': None, 'data_name': None}
    if request.method == 'POST':
        try:
            post_data = request.POST.get('post_data', None)
            post_data_dict = json.loads(post_data)
            currentAirportId = post_data_dict['airport']
            currentAirport = airport_baseData.objects.get(id=currentAirportId)
            if post_data_dict['runwayName']=='' or post_data_dict['runwayCode']=='':
                ret['message'] = '跑道名称和标志码不能为空。'
            else:
                runway_baseData.objects.create(
                    runwayName=post_data_dict['runwayName'],
                    runwayCode =post_data_dict['runwayCode'],
                    airport = currentAirport,
                    sizeOfRunway = post_data_dict['sizeOfRunway'],
                    sizeOfLiftingBelt = post_data_dict['sizeOfLiftingBelt'],
                    sizeOfBlastPad = post_data_dict['sizeOfBlastPad'],
                    widthOfShoulder = post_data_dict['widthOfShoulder'],
                    sizeOfSafetyZone = post_data_dict['sizeOfSafetyZone'],
                    operationCategory1 = post_data_dict['operationCategory1'],
                    operationCategory2 = post_data_dict['operationCategory2'],
                    takeoffDistance = post_data_dict['takeoffDistance'],
                    takeoffRunDistance = post_data_dict['takeoffRunDistance'],
                    runwayFrictionCoefficient = post_data_dict['runwayFrictionCoefficient'],
                    landingDistance = post_data_dict['landingDistance'],
                    accelerateStopDistance = post_data_dict['accelerateStopDistance'],
                    crossSlope = post_data_dict['crossSlope'],
                    effectiveLongitudinalSlope = post_data_dict['effectiveLongitudinalSlope'],
                    bulletinPCN = post_data_dict['bulletinPCN'],
                    shippingTime = post_data_dict['shippingTime'],
                    recordingTime = post_data_dict['recordingTime'],
                    updateTime=time.strftime('%Y-%m-%d %X', time.localtime())
                )

                ret['data'] = ''
                ret['message'] = '新增道面信息成功。'
                ret['status'] = True
        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'baseData/addRunway_Dialog.html')

def delRunwayBaseData(request):
    ret = {'status': False, 'message': '', 'data': None, 'data_name': None}
    if request.method == 'POST':
        try:
            post_data = request.POST.get('post_data', None)
            post_data_dict = json.loads(post_data)
            runwayId = post_data_dict['runwayId']
            if runwayId=='' or runwayId is None:
                ret['message'] = '参数获取错误。'
            else:
                runway_baseData.objects.filter(id = runwayId).delete()
                ret['message'] = '删除跑道信息成功。'
                ret['status'] = True
        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'baseData/addRunway_Dialog.html')

def alterRunwayData(request,runwayId):
    currentRunway = runway_baseData.objects.get(id=runwayId)
    context={
        'currentRunway': currentRunway
    }
    return render(request, 'baseData/alterRunway_Dialog.html', context)

def alterRunwayDataSubmit(request):
    ret = {'status': False, 'message': '', 'data': None, 'id': None}
    if request.method == 'POST':
        try:
            post_data = request.POST.get('post_data', None)
            post_data_dict = json.loads(post_data)
            runwayId = post_data_dict['runwayId']
            currentRunway = runway_baseData.objects.get(id=runwayId)
            if post_data_dict['runwayName'] == '' or post_data_dict['runwayCode'] == '':
                ret['message'] = '跑道名称和标志码不能为空。'
            else:
                runway_baseData.objects.filter(id=runwayId).update(
                    runwayName=post_data_dict['runwayName'],
                    runwayCode=post_data_dict['runwayCode'],
                    sizeOfRunway=post_data_dict['sizeOfRunway'],
                    sizeOfLiftingBelt=post_data_dict['sizeOfLiftingBelt'],
                    sizeOfBlastPad=post_data_dict['sizeOfBlastPad'],
                    widthOfShoulder=post_data_dict['widthOfShoulder'],
                    sizeOfSafetyZone=post_data_dict['sizeOfSafetyZone'],
                    operationCategory1=post_data_dict['operationCategory1'],
                    operationCategory2=post_data_dict['operationCategory2'],
                    takeoffDistance=post_data_dict['takeoffDistance'],
                    takeoffRunDistance=post_data_dict['takeoffRunDistance'],
                    runwayFrictionCoefficient=post_data_dict['runwayFrictionCoefficient'],
                    landingDistance=post_data_dict['landingDistance'],
                    accelerateStopDistance=post_data_dict['accelerateStopDistance'],
                    crossSlope=post_data_dict['crossSlope'],
                    effectiveLongitudinalSlope=post_data_dict['effectiveLongitudinalSlope'],
                    bulletinPCN=post_data_dict['bulletinPCN'],
                    shippingTime=post_data_dict['shippingTime'],
                    recordingTime=post_data_dict['recordingTime'],
                    updateTime=time.strftime('%Y-%m-%d %X', time.localtime())
                )
                data_models = runway_baseData.objects.get(id=runwayId)
                data =['跑道名称',data_models.runwayCode,
                       '跑道名称', data_models.runwayName,
                       '所属机场', data_models.airport.airportName,
                       '跑道尺寸', data_models.sizeOfRunway,
                       '升降带尺寸', data_models.sizeOfLiftingBelt,
                       '防吹坪尺寸', data_models.sizeOfBlastPad,
                       '道肩宽度', data_models.widthOfShoulder,
                       '端安全区尺寸', data_models.sizeOfSafetyZone,
                       '运行类别1', data_models.operationCategory1,
                       '运行类别2', data_models.operationCategory2,
                       '可用起飞距离', data_models.takeoffDistance,
                       '可用起飞滑跑距离', data_models.takeoffRunDistance,
                       '摩擦系数', data_models.runwayFrictionCoefficient,
                       '可用着陆距离', data_models.landingDistance,
                       '可用加速停止距离', data_models.accelerateStopDistance,
                       '横坡', data_models.crossSlope,
                       '有效纵坡', data_models.effectiveLongitudinalSlope,
                       '通报PCN', data_models.bulletinPCN,
                       '通航时间', data_models.shippingTime,
                       '记录时间', data_models.recordingTime,
                       '更新时间', data_models.updateTime
                       ]
                ret['data'] = data
                ret['id'] = runwayId
                ret['message'] = '修改道面信息成功。'
                ret['status'] = True
        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'baseData/alterRunway_Dialog.html')

def initSurfacePartitioniFrame(request):
    currentAirportId = request.COOKIES.get('currentAirportId', None)
    currentAirport = airport_baseData.objects.get(id=currentAirportId)
    part = PartTab.objects.filter(airport=currentAirport)
    context={
        'parts':part
    }
    return render(request, 'baseData/partitionInfo.html',context)

def searchPart(request):
    ret = {"code": 0, "msg": "", "count": None, "data": None}
    if request.method == 'POST':
        limit = request.POST['limit']
        page = request.POST['page']
        searchStr = '%'+request.POST.get('searchStr', '')+'%'
        currentAirportId = request.COOKIES.get('currentAirportId', None)

        currentAirport = airport_baseData.objects.get(id=currentAirportId)
        allPart = PartTab.objects.filter(airport=currentAirport)

        data = []

        for item in allPart:
            allArea = AreaTab.objects.filter(part=item).order_by('areaCode')
            areaCount = allArea.__len__()
            partArea=0
            structContain = []

            for area in allArea:
                belongCell = cellTab.objects.filter(area=area)
                if area.structCode not in structContain:
                    structContain.append(area.structCode)
                Area_area = 0
                # areacount = 0
                for item_ in belongCell:
                    cellArea = plateTab.objects.filter(cell=item_).aggregate(sumArea=Sum('area'))
                    Area_area += cellArea['sumArea'] if cellArea['sumArea']!=None else 0
                    # areacount = areacount + 1
                partArea+=Area_area


            item = {"id": item.id, "partCode": item.partCode, "partName": item.partName,"Area":str(partArea)+'m&sup2;',
                    "partDis": item.partDis, "airCode": item.airCode, "partLevel": item.partLevel,"updateTime":item.updateTime,
                    "containsAreaNum": str(areaCount), "containsStructureNum": str(structContain),"recordingTime":item.recordingTime}
            data.append(item)
        count = data.__len__()
        [currentpage, maxpage, minpage, maxpage] = commUtil.GetYeMa(page, limit, count)
        ret['count'] = count
        ret['data'] = data[minpage - 1:maxpage]
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'baseData/partitionInfo.html')

def initRoadSurfacePartitionInformation(request):
    allPart = PartTab.objects.filter().all()
    allArea = AreaTab.objects.filter().all()
    allcell = cellTab.objects.filter().all()
    firstPart = PartTab.objects.filter().all().order_by('partCode').first()
    firstArea = AreaTab.objects.filter(part=firstPart).order_by('areaCode').first()
    firstCell = cellTab.objects.filter(area=firstArea).order_by('cellCode').first()
    context={
        'parts':allPart,
        'areas':allArea,
        'cells':allcell,
        'firstArea':firstArea,
        'firstCell':firstCell
    }
    return render(request, 'baseData/roadSurfacePartitionInformation.html',context)

def addPart(request):
    return render(request, 'baseData/addPart_Dialog.html')

def addPartSubmit(request):
    ret = {'status': False, 'message': '', 'data': None,'flash':False}
    if request.method == 'POST':
        try:
            post_data = request.POST.get('post_data', None)
            post_data_dict = json.loads(post_data)
            currentAirportId = request.COOKIES.get('currentAirportId', None)
            currentAirport = airport_baseData.objects.get(id=currentAirportId)
            if post_data_dict['partCode'] == '' or post_data_dict['partName'] == '':
                ret['message'] = '部位名称和编码不能为空。'
            else:
                PartTab.objects.create(
                    airport=currentAirport,
                    partCode = post_data_dict['partCode'],
                    partName = post_data_dict['partName'],
                    partDis = post_data_dict['partDis'],
                    airCode = post_data_dict['airCode'],
                    containsAreaNum = post_data_dict['containsAreaNum'],
                    containsStructureNum = post_data_dict['containsStructureNum'],
                    partLevel = post_data_dict['partLevel'],
                    recordingTime = post_data_dict['recordingTime'],
                    updateTime=time.strftime('%Y-%m-%d %X', time.localtime())
                )
                ret['message'] = '添加部位信息成功。'
                ret['status'] = True
            allPart = PartTab.objects.filter().all()
            if allPart.__len__()==1:
                ret['flash'] = True
        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'baseData/addPart_Dialog.html')

def delPartSubmit(request):
    ret = {'status': False, 'message': '', 'data': None,'flash':False}
    if request.method == 'POST':
        try:
            post_data = request.POST.get('post_data', None)
            post_data_dict = json.loads(post_data)
            partId = post_data_dict['partId']

            if partId:
                currentPart = PartTab.objects.get(id=partId)
                area = AreaTab.objects.filter(part=currentPart)
                if area.__len__()>0:
                    ret['message'] = '检查出其拥有子项，请优先删除子项。'
                else:
                    PartTab.objects.filter(id=partId).delete()
                    ret['message'] = '删除部位信息成功。'
                    ret['status'] = True
                    allPart = PartTab.objects.filter().all()
                    if allPart.__len__()==0:
                        ret['flash'] = True
        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'baseData/partitionInfo.html')

def alterPart(request,partId):
    currentPart = PartTab.objects.get(id=partId)
    context={
        'currentPart': currentPart
    }
    return render(request, 'baseData/addPart_Dialog.html', context)

def alterPartSubmit(request):
    ret = {'status': False, 'message': '', 'data': None}
    if request.method == 'POST':
        try:
            post_data = request.POST.get('post_data', None)
            post_data_dict = json.loads(post_data)
            partId = post_data_dict['partId']
            if post_data_dict['partCode'] == '' or post_data_dict['partName'] == '':
                ret['message'] = '部位名称和编码不能为空。'
            else:
                PartTab.objects.filter(id=partId).update(
                    partCode=post_data_dict['partCode'],
                    partName=post_data_dict['partName'],
                    partDis=post_data_dict['partDis'],
                    airCode=post_data_dict['airCode'],
                    partLevel=post_data_dict['partLevel'],
                    recordingTime=post_data_dict['recordingTime'],
                    updateTime=time.strftime('%Y-%m-%d %X', time.localtime())
                )
                ret['message'] = '修改部位信息成功。'
                ret['status'] = True
        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'baseData/addPart_Dialog.html')

def searchArea(request):
    ret = {"code": 0, "msg": "", "count": None, "data": None}
    if request.method == 'POST':
        limit = request.POST['limit']
        page = request.POST['page']
        searchStr = '%'+request.POST.get('searchStr', '')+'%'
        currentAirportId = request.COOKIES.get('currentAirportId', None)
        currentAirport = airport_baseData.objects.get(id=currentAirportId)
        allPart = PartTab.objects.filter(airport=currentAirport)
        allArea=AreaTab.objects.filter(areaCode='')
        for item in allPart:
            allArea =allArea | AreaTab.objects.filter(part=item).order_by('areaCode')
        data = []
        for item in allArea:
            belongCell = cellTab.objects.filter(area=item)

            Area_area = 0
            count=0
            for item_ in belongCell:
                cellArea = plateTab.objects.filter(cell=item_).aggregate(sumArea = Sum('area'))
                Area_area+=cellArea['sumArea'] if cellArea['sumArea']!=None else 0
                count=count+1
            currentCom = structureComposition.objects.filter(structureCode=item.structCode).first()
            item = {"id": item.id, "areaCode": item.getDisplayAreaCode(), "areaDis": item.areaDis,
                    "partName": item.part.airCode + "(" + item.part.partName + ")", "areaStruct": item.areaStruct,
                    "area": str(Area_area) + 'm&sup2;', "cellNum": count, "recordingTime": item.recordingTime,
                    "updateTime": item.updateTime,
                    "structCode": "<h>" + currentCom.structureClass + "</h><h style='padding-left: 10px'>" + item.structCode + "</h><a style='cursor:pointer;padding-left:5px;' class='layui-icon' id='structCode' name='structCode'>&#xe64c;</a>"}
            data.append(item)
        count = data.__len__()
        [currentpage, maxpage, minpage, maxpage] = commUtil.GetYeMa(page, limit, count)
        ret['count'] = count
        ret['data'] = data[minpage - 1:maxpage]
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'baseData/partitionInfo.html')

def addArea(request):
    currentAirportId = request.COOKIES.get('currentAirportId', None)
    all = structureComposition.objects.order_by('structureClass','structureCode')
    allClass = structureComposition.objects.values('structureClass').distinct().order_by('structureClass')

    if currentAirportId:
        currentAirport = airport_baseData.objects.get(id=currentAirportId)
        allPart = PartTab.objects.filter(airport=currentAirport)
    context={
        'allPart':allPart,
        'structures': all,
        'allClass': allClass
    }
    return render(request, 'baseData/addArea_Dialog.html',context)

def addAreaSubmit(request):
    ret = {'status': False, 'message': '', 'data': None, 'flash': False}
    if request.method == 'POST':
        try:
            post_data = request.POST.get('post_data', None)
            post_data_dict = json.loads(post_data)

            if post_data_dict['areaCode'] == '' or post_data_dict['partId'] == '' or post_data_dict['structureCode'] == '':
                ret['message'] = '编码不能为空。且需选择所属部位。'
            else:
                currentpartId = post_data_dict['partId']
                currentPart = PartTab.objects.get(id=currentpartId)
                AreaTab.objects.create(
                    part=currentPart,
                    areaCode=post_data_dict['areaCode'],
                    areaDis=post_data_dict['areaDis'],
                    areaStruct=post_data_dict['areaStruct'],
                    recordingTime=post_data_dict['recordingTime'],
                    updateTime=time.strftime('%Y-%m-%d %X', time.localtime()),
                    structCode = post_data_dict['structureCode']
                )
                ret['message'] = '添加区域信息成功。'
                ret['status'] = True
            allPart = PartTab.objects.filter().all()
            if allPart.__len__() == 1:
                ret['flash'] = True
        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'baseData/addPart_Dialog.html')

def delAreaSubmit(request):
    ret = {'status': False, 'message': '', 'data': None, 'flash': False}
    if request.method == 'POST':
        try:
            post_data = request.POST.get('post_data', None)
            post_data_dict = json.loads(post_data)
            areaId = post_data_dict['areaId']
            if areaId:
                currentArea = AreaTab.objects.get(id=areaId)
                cell = cellTab.objects.filter(area=currentArea)
                if cell.__len__()>0:
                    ret['message'] = '检查出其拥有子项，请优先删除子项。'
                else:
                    AreaTab.objects.filter(id=areaId).delete()
                    ret['message'] = '删除区域信息成功。'
                    ret['status'] = True
            allArea = AreaTab.objects.filter().all()
            if allArea.__len__() == 0:
                ret['flash'] = True
        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'baseData/partitionInfo.html')

def alterArea(request,areaId):
    currentArea = AreaTab.objects.get(id=areaId)
    all = structureComposition.objects.order_by('structureClass','structureCode')
    allClass = structureComposition.objects.values('structureClass').distinct().order_by('structureClass')
    context={
        'currentArea': currentArea,
        'structures': all,
        'allClass': allClass

    }
    return render(request, 'baseData/addArea_Dialog.html', context)

def alterAreaSubmit(request):
    ret = {'status': False, 'message': '', 'data': None}
    if request.method == 'POST':
        try:
            post_data = request.POST.get('post_data', None)
            post_data_dict = json.loads(post_data)
            areaId = post_data_dict['areaId']
            if post_data_dict['areaCode'] == '' or post_data_dict['areaDis'] == '' or post_data_dict['structureCode'] == '':
                ret['message'] = '部位名称和位置不能为空。'
            else:
                AreaTab.objects.filter(id=areaId).update(
                    areaCode=post_data_dict['areaCode'],
                    areaDis=post_data_dict['areaDis'],
                    areaStruct=post_data_dict['areaStruct'],
                    recordingTime=post_data_dict['recordingTime'],
                    updateTime=time.strftime('%Y-%m-%d %X', time.localtime()),
                    structCode = post_data_dict['structureCode']
                )
                ret['message'] = '修改区域信息成功。'
                ret['status'] = True
        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'baseData/addArea_Dialog.html')

def updateList(request):
    ret = {'status': False, 'message': '', 'data': None}
    if request.method == 'POST':
        try:
            currentAirportId = request.COOKIES.get('currentAirportId', None)

            if currentAirportId:
                currentAirport = airport_baseData.objects.get(id=currentAirportId)
                allPart = PartTab.objects.filter(airport=currentAirport)
                data = []
                for part in allPart:
                    belongArea = AreaTab.objects.filter(part=part)
                    for item in belongArea:
                        area=[{"areaCode":item.areaCode,"areaDis":item.areaCode,"id":item.id}]
                    data.append({"name":part.partName,"areaData":area})

            ret['message'] = '修改区域信息成功。'
            ret['data']=data
            ret['status'] = True
        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'baseData/addArea_Dialog.html')

def initleftMenu(request):
    allPart = PartTab.objects.filter().all().order_by('partCode')
    allArea = AreaTab.objects.filter().all().order_by('areaCode')
    context={
        'parts':allPart,
        'areas':allArea
    }
    return render(request, 'baseData/part_areaList.html',context)

def initContent(request,areaId):
    currentArea = AreaTab.objects.get(id=areaId)
    context={
        'currentArea':currentArea
    }
    return render(request, 'baseData/cellList.html', context)


def searchCell(request):
    ret = {"code": 0, "msg": "", "count": None, "data": None}

    if request.method == 'POST':
        limit = request.POST['limit']
        page = request.POST['page']
        areaId =  request.POST['areaId']
        searchStr = request.POST.get('searchStr', '')
        currentArea = AreaTab.objects.filter(id=areaId)
        allCell= cellTab.objects.filter(area=currentArea).filter(cellCode__contains=searchStr)
        data = []
        for item in allCell:
            SumTotal = plateTab.objects.filter(cell=item).aggregate(sumArea = Sum('area'),sumPlateNum = Count('area'))
            item = {"id": item.id, "cellCode": item.getDisplayCellCode(), "area": item.area.getDisplayAreaCode()+'('+item.area.areaDis+')',
                    "part": item.area.part.airCode+'('+item.area.part.partName+')',"Area_":str(SumTotal['sumArea']) if SumTotal['sumArea'] else '0',
                    "banNum": str(SumTotal['sumPlateNum']), "recordingTime": item.recordingTime,"updateTime":item.updateTime}
            data.append(item)

        count = data.__len__()
        [currentpage, maxpage, minpage, maxpage] = commUtil.GetYeMa(page, limit, count)
        ret['count'] = count
        ret['data'] = data[minpage - 1:maxpage]
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'baseData/cellList.html')

def addCell(request,areaId):
    currentArea = AreaTab.objects.get(id=areaId)
    context={
        'currentArea':currentArea
    }
    return render(request, 'baseData/cell_Dialog.html',context)

def addCellSubmit(request):
    ret = {'status': False, 'message': '', 'data': None, 'flash': False}
    if request.method == 'POST':
        try:
            post_data = request.POST.get('post_data', None)
            post_data_dict = json.loads(post_data)

            if post_data_dict['cellCode'] == '' or post_data_dict['recordingTime'] == '':
                ret['message'] = '编码不能为空。且需需要填写记录日期。'
            else:
                area_id = post_data_dict['area_id']
                cruuentArea = AreaTab.objects.get(id=area_id)
                cellTab.objects.create(
                    area=cruuentArea,
                    cellCode=post_data_dict['cellCode'],
                    recordingTime=post_data_dict['recordingTime'],
                    updateTime=time.strftime('%Y-%m-%d %X', time.localtime())
                )
                ret['message'] = '添加单元信息成功。'
                ret['status'] = True
            # allPart = PartTab.objects.filter().all()
            # if allPart.__len__() == 1:
            #     ret['flash'] = True
        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'baseData/cell_Dialog.html')

def alterCell(request,areaId,cellId):
    currentCell = cellTab.objects.get(id=cellId)
    context={
        'currentCell': currentCell
    }
    return render(request, 'baseData/cell_Dialog.html', context)

def alterCellSubmit(request):
    ret = {'status': False, 'message': '', 'data': None}
    if request.method == 'POST':
        try:
            post_data = request.POST.get('post_data', None)
            post_data_dict = json.loads(post_data)

            if post_data_dict['cellCode'] == '' or post_data_dict['recordingTime'] == '':
                ret['message'] = '编码不能为空。且需需要填写记录日期。'
            else:
                cellId = post_data_dict['cellId']
                cellTab.objects.filter(id=cellId).update(
                    cellCode=post_data_dict['cellCode'],
                    recordingTime = post_data_dict['recordingTime'],
                    updateTime=time.strftime('%Y-%m-%d %X', time.localtime())
                )
                ret['message'] = '修改单元信息成功。'
                ret['status'] = True
        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'baseData/cell_Dialog.html')

def delCellSubmit(request):
    ret = {'status': False, 'message': '', 'data': None, 'flash': False}
    if request.method == 'POST':
        try:
            post_data = request.POST.get('post_data', None)
            post_data_dict = json.loads(post_data)
            cellId = post_data_dict['cellId']
            if cellId:
                currentCell = cellTab.objects.get(id=cellId)
                plate = plateTab.objects.filter(cell=currentCell)
                if plate.__len__()>0:
                    ret['message'] = '检查出其拥有子项，请优先删除子项。'
                else:
                    cellTab.objects.filter(id=cellId).delete()
                    ret['message'] = '删除单元信息成功。'
                    ret['status'] = True
                    allCell = cellTab.objects.filter().all()
                    if allCell.__len__() == 0:
                        ret['flash'] = True
        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'baseData/roadSurfacePartitionInformation.html')

def initleftMenu_plate(request):
    allPart = PartTab.objects.filter().all().order_by('partCode')
    allArea = AreaTab.objects.filter().all().order_by('areaCode')
    allcell = cellTab.objects.filter().all().order_by('cellCode')
    context={
        'parts':allPart,
        'areas':allArea,
        'cells':allcell
    }
    return render(request, 'baseData/part_area_plateList.html',context)

def initContent_plate(request,cellId):
    currentCell = cellTab.objects.get(id=cellId)
    context={
        'currentCell':currentCell
    }
    return render(request, 'baseData/plateList.html', context)

def searchPlate(request):
    ret = {"code": 0, "msg": "", "count": None, "data": None}

    if request.method == 'POST':
        limit = request.POST['limit']
        page = request.POST['page']
        cellId =  request.POST['cellId']
        searchStr = request.POST.get('searchStr', '')
        index = searchStr.strip().lstrip().find(',')
        currentCell = cellTab.objects.get(id=cellId)
        if searchStr=='':
            allPlate = plateTab.objects.filter(cell=currentCell)
        else:
            rowstr = searchStr.strip().lstrip()[0:index]
            colstr = searchStr.strip().lstrip()[index+1:len(searchStr)]
            if rowstr=='*' and colstr.isdigit():
                allPlate = plateTab.objects.filter(cell=currentCell).filter(colNo=colstr)
            elif colstr=='*' and rowstr.isdigit():
                allPlate = plateTab.objects.filter(cell=currentCell).filter(rowNo=rowstr)
            elif colstr.isdigit() and rowstr.isdigit():
                allPlate = plateTab.objects.filter(cell=currentCell).filter(rowNo=rowstr,colNo=colstr)
            else:
                allPlate = plateTab.objects.filter(cell=currentCell).filter(rowNo=searchStr)



        data = []
        for item in allPlate:
            item = {"id": item.id, "cell": item.cell.getDisplayCellCode(), "rowNo": item.rowNo,
                    "colNo": item.colNo,"platelength":item.platelength,
                    "width": item.width, "area": str(item.area),"shape":item.shape,"recordingTime":item.recordingTime,"updateTime":item.updateTime}
            data.append(item)

        count = data.__len__()
        [currentpage, maxpage, minpage, maxpage] = commUtil.GetYeMa(page, limit, count)
        ret['count'] = count
        ret['data'] = data[minpage - 1:maxpage]
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'baseData/plateList.html')


def addPlate(request,cellId):
    currentCell = cellTab.objects.get(id=cellId)
    context={
        'currentCell':currentCell
    }
    return render(request, 'baseData/plate_Dialog.html',context)

def addPlateSubmit(request):
    ret = {'status': False, 'message': '', 'data': None, 'flash': False}
    if request.method == 'POST':
        try:
            post_data = request.POST.get('post_data', None)
            post_data_dict = json.loads(post_data)

            if post_data_dict['rowNo'] == '' or post_data_dict['colNo'] == '':
                ret['message'] = '此项不能为空。'
            else:
                cellId = post_data_dict['cellId']
                cruuentCell = cellTab.objects.get(id=cellId)
                plateTab.objects.create(
                    cell=cruuentCell,
                    rowNo = post_data_dict['rowNo'],
                    colNo = post_data_dict['colNo'],
                    platelength = post_data_dict['platelength'],
                    width = post_data_dict['width'],
                    area = post_data_dict['area'],
                    shape = post_data_dict['shape'],
                    recordingTime=post_data_dict['recordingTime'],
                    updateTime=time.strftime('%Y-%m-%d %X', time.localtime())
                )
                ret['message'] = '添加板块信息成功。'
                ret['status'] = True
        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'baseData/plate_Dialog.html')

def delPlateSubmit(request):
    ret = {'status': False, 'message': '', 'data': None, 'flash': False}
    if request.method == 'POST':
        try:
            post_data = request.POST.get('post_data', None)
            post_data_dict = json.loads(post_data)
            plateId = post_data_dict['plateId']
            if plateId:
                plateTab.objects.filter(id=plateId).delete()
                ret['message'] = '删除板块信息成功。'
                ret['status'] = True
        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'baseData/plateList.html.html')

def alterPlate(request,cellId,plateId):
    currentPlate = plateTab.objects.get(id=plateId)
    context={
        'currentPlate': currentPlate
    }
    return render(request, 'baseData/plate_Dialog.html', context)

def alterPlateSubmit(request):
    ret = {'status': False, 'message': '', 'data': None}
    if request.method == 'POST':
        try:
            post_data = request.POST.get('post_data', None)
            post_data_dict = json.loads(post_data)

            if post_data_dict['rowNo'] == '' or post_data_dict['colNo'] == '':
                ret['message'] = '此项不能为空。'
            else:
                plateId = post_data_dict['plateId']
                plateTab.objects.filter(id=plateId).update(
                    rowNo =  post_data_dict['rowNo'],
                    colNo = post_data_dict['colNo'],
                    platelength = post_data_dict['platelength'],
                    width = post_data_dict['width'],
                    area = post_data_dict['area'],
                    shape = post_data_dict['shape'],
                    recordingTime = post_data_dict['recordingTime'],
                    updateTime=time.strftime('%Y-%m-%d %X', time.localtime())
                )
                ret['message'] = '修改板块信息成功。'
                ret['status'] = True
        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'baseData/plate_Dialog.html')


# # # 道面结构类型
def initPavementStructureType(request):
    all = structureComposition.objects.order_by('structureClass','structureCode')
    allClass = structureComposition.objects.values('structureClass').distinct().order_by('structureClass')
    firstClass = allClass.first()
    firstItem = all.first()
    context={
        'structures':all,
        'allClass':allClass,
        'firstClass':firstClass,
        'firstItem':firstItem
    }
    return render(request, 'baseData/structure/pavementStructureType.html',context)

def initStructrueMenu(request):
    all = structureComposition.objects.order_by('structureClass','structureCode')
    allClass = structureComposition.objects.values('structureClass').distinct().order_by('structureClass')
    context={
        'structures':all,
        'allClass':allClass
    }
    return render(request, 'baseData/structure/structrueMenu.html',context)

def addStructrueCombine(request):
    return render(request, 'baseData/structure/structureCombine_Dialog.html')

def addClassSubmit(request):
    ret = {'status': False, 'message': '', 'data': None, 'flash': False}
    if request.method == 'POST':
        try:
            post_data = request.POST.get('post_data', None)
            post_data_dict = json.loads(post_data)

            if post_data_dict['structureClass'] == '' or post_data_dict['structureCode'] == '':
                ret['message'] = '此项不能为空。'
            else:
                structureComposition.objects.create(
                    structureClass=post_data_dict['structureClass'],
                    structureCode=post_data_dict['structureCode'],
                )
                ret['message'] = '添加结构组合信息成功。'
                ret['status'] = True
        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'baseData/structure/structureCombine_Dialog.html')

def initStructrueContent(request,structureClass,structureCode):
    currentCombine = structureComposition.objects.get(structureClass=structureClass,structureCode=structureCode)
    context={
        'currentCombine':currentCombine
    }
    return render(request, 'baseData/structure/structureList.html', context)


def searchLayer(request):
    ret = {"code": 0, "msg": "", "count": None, "data": None}

    if request.method == 'POST':
        limit = request.POST['limit']
        page = request.POST['page']
        structureCode = request.POST['structureCode']
        searchStr = request.POST.get('searchStr', '')
        currentStructure = structure.objects.filter(structureCode=structureCode).filter(materialName__contains=searchStr).order_by('layerCode')

        LAYER = {
            "1":"第一层",
            "2": "第二层",
            "3": "第三层",
            "4": "第四层",
            "5": "第五层",
            "6": "第六层",
            "7": "第七层",
        }
        data = []
        for item in currentStructure:
            item = {"id": item.id, "layerCode":item.layerCode,"layer": LAYER.get(item.layerCode),"materialName": item.materialName,
                    "thickness": item.thickness, "elasticModulus": item.elasticModulus,
                    "CBR": item.CBR, "poissonRatio": item.poissonRatio, "recordingTime": item.recordingTime,"updateTime": item.updateTime}
            data.append(item)

        count = data.__len__()
        [currentpage, maxpage, minpage, maxpage] = commUtil.GetYeMa(page, limit, count)
        ret['count'] = count
        ret['data'] = data[minpage - 1:maxpage]
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'baseData/structure/structureList.html')

def addLayer(request,structureClass,structureCode):
    currentStructure = structure.objects.filter(structureCode=structureCode)
    LAYER =[
        {"code": "1", "name": "第一层","disable":"false"},
        {"code": "2", "name": "第二层","disable":"false"},
        {"code": "3", "name": "第三层","disable":"false"},
        {"code": "4", "name": "第四层","disable":"false"},
        {"code": "5", "name": "第五层","disable":"false"},
        {"code": "6", "name": "第六层","disable":"false"},
        {"code": "7", "name": "第七层","disable":"false"},
    ]
    for item in currentStructure:
        for layer in LAYER:
            if item.layerCode==layer['code']:
                layer['disable']="true"
    context={
        'structureCode':structureCode,
        'LAYER':LAYER
    }
    return render(request, 'baseData/structure/layer_Dialog.html',context)

def showLayerPic(request,structureClass,structureCode):
    currentStructure = structure.objects.filter(structureCode=structureCode).order_by('layerCode')
    LAYER = {
        "1": "第一层",
        "2": "第二层",
        "3": "第三层",
        "4": "第四层",
        "5": "第五层",
        "6": "第六层",
        "7": "第七层",
    }
    data=[]
    for item in currentStructure:
        layerData = {'name':LAYER.get(item.layerCode)+'('+item.materialName+')','value':item.thickness}
        data.append(layerData)
    context={
        'structureCode':structureCode,
        'data':data
    }
    return render(request, 'baseData/structure/layer_Pic.html', context)

def alterLayer(request,structureClass,structureCode,layerId):
    currentStructure = structure.objects.filter(structureCode=structureCode)
    LAYER = [
        {"code": "1", "name": "第一层", "disable": "false"},
        {"code": "2", "name": "第二层", "disable": "false"},
        {"code": "3", "name": "第三层", "disable": "false"},
        {"code": "4", "name": "第四层", "disable": "false"},
        {"code": "5", "name": "第五层", "disable": "false"},
        {"code": "6", "name": "第六层", "disable": "false"},
        {"code": "7", "name": "第七层", "disable": "false"},
    ]
    for item in currentStructure:
        for layer in LAYER:
            if item.layerCode == layer['code']:
                layer['disable'] = "true"
    currentLayer = structure.objects.get(id=int(layerId))
    context = {
        'currentLayer': currentLayer,
        'LAYER': LAYER
    }
    return render(request, 'baseData/structure/layer_Dialog.html', context)

def alterStructureSubmit(request):
    ret = {'status': False, 'message': '', 'data': None}
    if request.method == 'POST':
        try:
            post_data = request.POST.get('post_data', None)
            post_data_dict = json.loads(post_data)

            if post_data_dict['materialName'] == '' \
                    or not post_data_dict['thickness'].isdigit() or not post_data_dict['elasticModulus'].replace('.', '', 1).isdigit() \
                    or not post_data_dict['CBR'].replace('.', '', 1).isdigit() or not post_data_dict['poissonRatio'].replace('.', '', 1).isdigit() \
                    or post_data_dict['recordingTime'] == '':
                ret['message'] = '此项不能为空。'
            else:
                layerId = post_data_dict['layerId']
                structure.objects.filter(id=layerId).update(
                    materialName = post_data_dict['materialName'],
                    thickness = post_data_dict['thickness'],
                    elasticModulus = post_data_dict['elasticModulus'],
                    CBR = post_data_dict['CBR'],
                    poissonRatio = post_data_dict['poissonRatio'],
                    recordingTime=post_data_dict['recordingTime'],
                    updateTime=time.strftime('%Y-%m-%d %X', time.localtime())
                )
                ret['message'] = '修改层位信息成功。'
                ret['status'] = True
        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'baseData/structure/layer_Dialog.html')

def addStructureSubmit(request):
    ret = {'status': False, 'message': '', 'data': None, 'flash': False}
    if request.method == 'POST':
        try:
            post_data = request.POST.get('post_data', None)
            post_data_dict = json.loads(post_data)
            if post_data_dict['Layer'] == '' or post_data_dict['materialName'] == '' \
                    or not post_data_dict['thickness'].replace('.', '', 1).isdigit() or not post_data_dict['elasticModulus'].replace('.', '', 1).isdigit() \
                    or not post_data_dict['CBR'].replace('.', '', 1).isdigit() or not post_data_dict['poissonRatio'].replace('.', '', 1).isdigit() \
                    or post_data_dict['recordingTime'] == '':
                ret['message'] = '此项不能为空。'
            else:
                structure.objects.create(
                    structureCode=post_data_dict['structureCode'],
                    layerCode = post_data_dict['Layer'],
                    materialName = post_data_dict['materialName'],
                    thickness = post_data_dict['thickness'],
                    elasticModulus = post_data_dict['elasticModulus'],
                    CBR = post_data_dict['CBR'],
                    poissonRatio = post_data_dict['poissonRatio'],
                    recordingTime=post_data_dict['recordingTime'],
                    updateTime=time.strftime('%Y-%m-%d %X', time.localtime())
                )
                ret['message'] = '添加层位信息成功。'
                ret['status'] = True
        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'baseData/structure/layer_Dialog.html')

def delLayerSubmit(request):
    ret = {'status': False, 'message': '', 'data': None}
    if request.method == 'POST':
        try:
            post_data = request.POST.get('post_data', None)
            post_data_dict = json.loads(post_data)
            id = post_data_dict['layerId']
            currentLayer = structure.objects.get(id=id)
            currentLayerCode = currentLayer.layerCode
            currentStructureCode = currentLayer.structureCode
            if id:
                belwLayer = structure.objects.filter(structureCode=currentStructureCode).filter(layerCode__gt=currentLayerCode)
                for item in belwLayer:
                    item.layerCode=str(int(item.layerCode)-1)
                    item.save()
                currentLayer.delete()
                ret['message'] = '删除层位信息成功。'
                ret['status'] = True
        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'baseData/structure/structureList.html')



@transaction.atomic
def moveUpLayerSubmit(request):
    ret = {'status': False, 'message': '', 'data': None}
    if request.method == 'POST':
        try:
            post_data = request.POST.get('post_data', None)
            post_data_dict = json.loads(post_data)
            id = post_data_dict['layerId']
            currentLayer = structure.objects.get(id=id)
            currentLayerCode = currentLayer.layerCode
            currentStructureCode = currentLayer.structureCode
            # 获取 同 组合 最大、小层位
            # allLayer = structure.objects.get(structureCode=currentStructureCode)
            # maxlayer = '1'
            # for item in allLayer:
            #     if item.layerCode>maxlayer:
            #         maxlayer=item.layerCode
            if currentLayerCode=='1':
                ret['message'] = '已经是顶层了，无法完成操作。'
            else:
                beforeLayer = structure.objects.filter(structureCode=currentStructureCode).filter(layerCode=str(int(currentLayerCode)-1))
                if beforeLayer:
                    beforeLayer_true = structure.objects.filter(structureCode=currentStructureCode).get(layerCode=str(int(currentLayerCode)-1))
                    beforeLayer_true.layerCode = str(int(beforeLayer_true.layerCode)+1)
                    beforeLayer_true.save()
                currentLayer.layerCode=str(int(currentLayerCode)-1)
                currentLayer.save()
                ret['status'] = True
        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'baseData/structure/structureList.html')

@transaction.atomic
def moveDownLayerSubmit(request):
    ret = {'status': False, 'message': '', 'data': None}
    if request.method == 'POST':
        try:
            post_data = request.POST.get('post_data', None)
            post_data_dict = json.loads(post_data)
            id = post_data_dict['layerId']
            currentLayer = structure.objects.get(id=id)
            currentLayerCode = currentLayer.layerCode
            currentStructureCode = currentLayer.structureCode
            # 获取 同 组合 最大、小层位
            allLayer = structure.objects.filter(structureCode=currentStructureCode)
            maxlayer = '1'
            for item in allLayer:
                if item.layerCode>maxlayer:
                    maxlayer=item.layerCode
            if currentLayerCode == maxlayer:
                ret['message'] = '已经是底层了，无法完成操作。'
            else:
                afterLayer = structure.objects.filter(structureCode=currentStructureCode).filter(
                    layerCode=str(int(currentLayerCode) + 1))
                if afterLayer:
                    afterLayer_true = structure.objects.filter(structureCode=currentStructureCode).get(
                        layerCode=str(int(currentLayerCode) + 1))
                    afterLayer_true.layerCode = str(int(afterLayer_true.layerCode) - 1)
                    afterLayer_true.save()
                currentLayer.layerCode = str(int(currentLayerCode) + 1)
                currentLayer.save()
                ret['status'] = True
        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'baseData/structure/structureList.html')

# 首页 提醒页
def indexPage(request):
    # username = request.user.username
    # SystemMenu =[
    #     {'isCurrent': 'true', 'href': '', 'icon': '&#xe6ed;', 'menu':
    #         [{'isCurrent': 'false', 'href': '', 'icon': '&#xe61c;', 'title': '主页',
    #           'children': [
    #               {'isCurrent': 'false', 'href': 'index/', 'icon': '', 'title': '首页', 'children': []}]
    #           },
    #          {'isCurrent': 'true', 'href': '', 'icon': '&#xe688;', 'title': '权限管理',
    #           'children': [{'isCurrent': 'true', 'href': 'sysManage/authorization/userManag/', 'icon': '', 'title': '员工管理', 'children': []}, {'isCurrent': 'false', 'href': 'sysManage/authorization/roleManag/', 'icon': '', 'title': '角色管理', 'children': []}]}, {'isCurrent': 'false', 'href': '', 'icon': '&#xe62d;', 'title': '基础资料管理', 'children': [{'isCurrent': 'false', 'href': 'sysManage/baseData/airportBasicInformation/', 'icon': '', 'title': '机场基本信息', 'children': []}, {'isCurrent': 'false', 'href': 'sysManage/baseData/runwayBasicInformation/', 'icon': '', 'title': '跑道基本信息', 'children': []}, {'isCurrent': 'false', 'href': 'sysManage/baseData/roadSurfacePartitionInformation/', 'icon': '', 'title': '道面分区信息', 'children': []}, {'isCurrent': 'false', 'href': 'sysManage/baseData/pavementStructureType/', 'icon': '', 'title': '道面结构类型', 'children': []}]}], 'title': '系统管理'}, {'isCurrent': '', 'href': 'http://www.baidu.com', 'icon': '&#xe699;', 'menu': [{}], 'title': '土面区管理'}, {'isCurrent': '', 'href': '', 'icon': '&#xe6ca;', 'menu': [{'isCurrent': 'true', 'href': '', 'icon': '&#xe6ca;', 'title': '合同与项目管理', 'children': [{'isCurrent': 'true', 'href': 'contractManagement/projects/projectManage/', 'icon': '', 'title': '项目管理', 'children': []}, {'isCurrent': 'false', 'href': '', 'icon': '', 'title': '分类管理项目', 'children': []}, {'isCurrent': 'false', 'href': 'contractManagement/contracts/contractManage/', 'icon': '', 'title': '合同管理', 'children': []}]}], 'title': '合同管理'}, {'isCurrent': '', 'href': '', 'icon': '&#xe645;', 'menu': [{'isCurrent': 'true', 'href': '', 'icon': '&#xe6b8;', 'title': '计划', 'children': [{'isCurrent': 'true', 'href': 'evaluationManagement/damage/surveyPlan/', 'icon': '', 'title': '计划列表', 'children': []}]}, {'isCurrent': 'false', 'href': '', 'icon': '&#xe6c9;', 'title': '道面损坏调查', 'children': [{'isCurrent': 'false', 'href': 'evaluationManagement/damage/damageRecordsAndEvaluation/', 'icon': '', 'title': '损坏数据与评价', 'children': []}, {'isCurrent': 'false', 'href': 'evaluationManagement/damage/damageStatistics/', 'icon': '', 'title': '损坏数据统计', 'children': []}]}, {'isCurrent': 'false', 'href': '', 'icon': '&#xe6c9;', 'title': '道面弯沉评价', 'children': [{'isCurrent': 'false', 'href': 'evaluationManagement/deflection/RecordsAndEvaluation/', 'icon': '', 'title': '道面弯沉数据与评价', 'children': []}]}, {'isCurrent': 'false', 'href': '', 'icon': '&#xe6c9;', 'title': '道面平整度评价', 'children': [{'isCurrent': 'false', 'href': 'evaluationManagement/planeness/RecordsAndEvaluation/', 'icon': '', 'title': '道面平整度数据与评价', 'children': []}]}], 'title': '道面评价管理'}]
    # context = {
    #     'username': username,
    #     'SystemMenu': SystemMenu
    # }
    return render(request, 'pageIndex.html')

def changeToPdf(request):
    import pdfkit,os
    print(request.get_host())
    config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files (x86)\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    pdfkit.from_url(request.get_host()+'/component/index/', 'upload/lsDir/out.pdf',configuration=config)
    return render(request, 'pageIndex.html')