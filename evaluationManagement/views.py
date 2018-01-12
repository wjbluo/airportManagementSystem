from django.shortcuts import render,HttpResponse
from .models import *
import datetime
import os
from main.models import *
import json
from django.db.models import Sum,Count
from django.conf import settings
import xlrd
from utils import xlrd_read_excel,numUtil,strTrans,commUtil,PCIcal
from django.http import StreamingHttpResponse
from django.db.models import Q
from django.db import connection
# Create your views here.

def initsurveyPlan(request):
    firstPlan = surveyPlan.objects.all().order_by('-year', '-surveyPlanCode').first()
    context = {
        'firstPlan':firstPlan
    }
    return render(request, 'evaluationManagement/plan/surveyPlan.html', context)

def planMenu(request):
    searchStr = request.GET.get('searchStr', '')
    allplan = surveyPlan.objects.filter(surveyPlanCode__contains=searchStr).order_by('-year','-surveyPlanCode').values('surveyPlanCode','year')
    allyear = allplan.values('year').distinct().order_by('-year')
    context={
        'allplan':allplan,
        'allyear':allyear
    }
    return render(request, 'evaluationManagement/plan/planMenu.html', context)

def addPlan(request):
    define_PPID =datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    context={
        'define_PPID':define_PPID
    }
    return render(request, 'evaluationManagement/plan/plan_Dialog.html', context)

def selectObject(request):
    currentAirportId = request.COOKIES.get('currentAirportId',None)
    currentAirport = airport_baseData.objects.get(id=currentAirportId)
    Nodes=[]
    parentNodes = []
    if currentAirport:
        allPart = currentAirport.parttab_set.all()
        for part in allPart:
            Nodes.append({"id":'p'+str(part.id),"pId":0,"name":part.airCode+'('+part.partName+')',"open":"true"})
            parentNodes.append({"id":'p'+str(part.id),"pId":0,"name":part.airCode+'('+part.partName+')',"open":"true"})
            Areas = part.areatab_set.all()
            for area in Areas:
                Nodes.append({"id": area.id, "pId": 'p'+str(area.part.id), "name": area.getDisplayAreaCode() +'('+ area.areaDis+')', "open": "true"})
                parentNodes.append({"id": area.id, "pId": 'p'+str(area.part.id), "name": area.getDisplayAreaCode() + '(' + area.areaDis + ')',
                              "open": "true","nocheck":"true"})
    context={
        'Nodes':Nodes,
        'parentNodes':parentNodes
    }
    return render(request, 'evaluationManagement/plan/setObject_Dialog.html', context)

def setObject(request):
    ret = {'status': False, 'message': '', 'data': None}
    if request.method == 'POST':
        try:
            post_data = request.POST.get('post_data', None)
            post_data_dict = json.loads(post_data)

            dataForSurface = post_data_dict['data1']
            dataForStruct = post_data_dict['data2']
            dataForPlaneness = post_data_dict['data3']
            dataForAllArea =  post_data_dict['allareadata']

            allarea = AreaTab.objects.filter(updateTime='xxxx-xx-xx')
            for AreaId in dataForAllArea:
                area = AreaTab.objects.filter(id=AreaId)
                allarea=allarea|area
            allarea=allarea.distinct().order_by('areaCode')
            data=[]
            cellNum = 0
            totalArea = 0
            part = []
            for area in allarea:
                if area.part_id not in part:
                    part.append(area.part_id)
                cells = area.celltab_set.all()
                cellNum+=cells.__len__()
                Area_area = 0
                for item_ in cells:
                    cellArea = plateTab.objects.filter(cell=item_).aggregate(sumArea=Sum('area'))
                    Area_area += cellArea['sumArea']
                totalArea+=Area_area
                dir = { "areaId":area.id,
                        "areaName":area.getDisplayAreaCode()+'('+area.areaDis+')',
                         "partName":area.part.partCode+'('+area.part.partName+')',
                         "cellNum":str(cells.__len__()),
                         "area":str(Area_area),
                         "structure":area.structCode,
                         "EvaContent":''
                         }
                if area.id in dataForSurface:
                    dir["EvaContent"] = dir["EvaContent"]+'1'
                if area.id in dataForStruct:
                    dir["EvaContent"] = dir["EvaContent"]+'2'
                if area.id in dataForPlaneness:
                    dir["EvaContent"] =dir["EvaContent"]+ '3'

                data.append(dir)
            ret['data']=data
            ret['status'] = True
            ret.update({"partNum":str(part.__len__()),"areaNum":str(allarea.__len__()),"cellNum":str(cellNum),"totalArea":str(totalArea)})
        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'evaluationManagement/plan/setObject_Dialog.html')

def addPlanSubmit(request):
    ret = {'status': False, 'message': '', 'data': None,'planId':None}
    if request.method == 'POST':
        try:
            post_data = request.POST.get('post_data', None)
            post_data_dict = json.loads(post_data)
            if post_data_dict['gridData']==[]  or post_data_dict['startTime']=='' or post_data_dict['startTime']=='' or post_data_dict['EvaUnit'] == '' or post_data_dict['desc'] == '':

                ret['message']='请将表格补充完整。'
            else:
                gridData = post_data_dict['gridData']
                if gridData:
                    year = post_data_dict['planId'][0:4]
                    surveyPlan.objects.create(
                        surveyPlanCode=post_data_dict['planId'],
                        year=year,
                        startTime=post_data_dict['startTime'],
                        endTime=post_data_dict['endTime'],
                        evaluationUnit=post_data_dict['EvaUnit'],
                        remark=post_data_dict['desc'],
                    )
                    for item in gridData:
                        currentArea = AreaTab.objects.get(id=item['areaId'])
                        assessmentItems.objects.create(
                            surveyPlan_id=post_data_dict['planId'],
                            area = currentArea,
                            assessmentItem = item['EvaContent'],
                        )
                        # pass

                    ret['data'] = ''
                    ret['planId'] = post_data_dict['planId']
                    ret['message'] = '保存成功！'
                    ret['status'] = True
                else:
                    ret['message'] = 'gridData为空'
        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'evaluationManagement/plan/showPlan.html')

def showPlan(request,surveyPlanCode):
    currentPlan = surveyPlan.objects.get(surveyPlanCode=surveyPlanCode)
    allItem = currentPlan.assessmentitems_set.all()
    data = []
    part=[]
    cellNum=0
    totalArea=0
    for item in allItem:
        if item.area.part_id not in part:
            part.append(item.area.part_id)
        cells = item.area.celltab_set.all()
        cellNum += cells.__len__()
        Area_area = 0
        for item_ in cells:
            cellArea = plateTab.objects.filter(cell=item_).aggregate(sumArea=Sum('area'))
            Area_area += cellArea['sumArea']
        totalArea += Area_area
        currentPart = item.area.part
        dir = {"areaId": item.area.id,
               "areaName": item.area.getDisplayAreaCode() + '(' + item.area.areaDis + ')',
               "partName": item.area.part.partCode + '(' + item.area.part.partName + ')',
               "cellNum": str(cells.__len__()),
               "area": str(Area_area),
               "structure": item.area.structCode,
               "EvaContent": item.assessmentItem
               }
        data.append(dir)
    context={
        'currentPlan':currentPlan,
        'partNum':part.__len__(),
        'areaNum':allItem.__len__(),
        'cellNum':cellNum,
        'EvaArea':totalArea,
        'data':data
    }
    return render(request, 'evaluationManagement/plan/showPlan.html', context)

# # 损坏记录与评价
def initDamageRecordsAndEvaluation(request):
    allOperArea = assessmentItems.objects.filter(assessmentItem__contains='1').order_by('-surveyPlan_id','area_id')#  1 指的是损坏数据
    allPlan = surveyPlan.objects.filter(surveyPlanCode__in=allOperArea.values('surveyPlan_id')).order_by('-surveyPlanCode')
    firstPlan = allPlan.first()
    firstOperArea = allOperArea.first()
    if firstPlan:
        context={
            'allPlan':allPlan,
            'allOperArea':allOperArea,
            'firstPlan':firstPlan,
            'firstOperArea':firstOperArea,
        }
        return render(request, 'evaluationManagement/damage/initdamageFrame.html',context)
    return HttpResponse("请先添加计划。")

def damageMenu(request,Type):
    allOperArea = assessmentItems.objects.filter(assessmentItem__contains=Type).order_by('-surveyPlan_id','area__areaCode')#  1 指的是损坏数据
    allPlan = surveyPlan.objects.filter(surveyPlanCode__in=allOperArea.values('surveyPlan_id')).order_by('-surveyPlanCode')

    firstPlan = allPlan.first()
    firstOperArea = allOperArea.first()

    if Type=='1':
        data_damage = []
        for item in allOperArea:
            if_damageData = damageData.objects.filter(surveyPlan=item.surveyPlan,area=item.area)
            if if_damageData:
                dic={'surveyPlan_id':item.surveyPlan_id,'area':item.area,'flag':1}
            else:
                dic = {'surveyPlan_id': item.surveyPlan_id, 'area': item.area, 'flag': 0}
            data_damage.append(dic)
        context = {
            'allPlan': allPlan,
            'allOperArea': data_damage,
            'firstPlan': firstPlan,
            'firstOperArea': firstOperArea,
            'type': Type
        }
        return render(request, 'evaluationManagement/damage/damageMenu.html',context)
    if Type=='2':
        data_deflect = []
        for item in allOperArea:
            if_deflectData = deflectData.objects.filter(surveyPlan=item.surveyPlan,area=item.area)
            if if_deflectData:
                dic={'surveyPlan_id':item.surveyPlan_id,'area':item.area,'flag':1}
            else:
                dic = {'surveyPlan_id': item.surveyPlan_id, 'area': item.area, 'flag': 0}
            data_deflect.append(dic)
        context = {
            'allPlan': allPlan,
            'allOperArea': data_deflect,
            'firstPlan': firstPlan,
            'firstOperArea': firstOperArea,
            'type': Type
        }
        return render(request, 'evaluationManagement/deflection/deflectionMenu.html',context)
    if Type=='3':
        part=[]
        for operArea in allOperArea:
            dict = {'surveyPlanCode':operArea.surveyPlan.surveyPlanCode,'part':operArea.area.part.airCode+'('+operArea.area.part.partCode+')','partId':operArea.area.part.id}
            if dict not in part:
                part.append(dict)
        context = {
            'allPlan': allPlan,
            'firstPlan':firstPlan,
            'firstOperArea':firstOperArea,
            'part': part,
            'type': Type
        }
        return render(request, 'evaluationManagement/planeness/planenessMenu.html',context)

def statMenu(request,Type):
    allOperArea = assessmentItems.objects.filter(assessmentItem__contains=Type).order_by('-surveyPlan_id','area__areaCode')#  1 指的是损坏数据
    allPlan = surveyPlan.objects.filter(surveyPlanCode__in=allOperArea.values('surveyPlan_id')).order_by('-surveyPlanCode')
    firstPlan = allPlan.first()
    firstOperArea = allOperArea.first()
    context={
        'allPlan':allPlan,
        'allOperArea':allOperArea,
        'firstPlan':firstPlan,
        'firstOperArea':firstOperArea,
        'type':Type
    }
    if Type=='1':
        return render(request, 'evaluationManagement/damage/statMenu.html', context)

def damageStat(request,surveyPlanCode,areaId):
    currentPlan = surveyPlan.objects.get(surveyPlanCode=surveyPlanCode)
    currentItems = assessmentItems.objects.filter(surveyPlan=currentPlan,assessmentItem__contains='1')
    currentArea = AreaTab.objects.get(id=areaId)
    damagePara = parameterTab.objects.filter(parameterType='damageType').order_by('id')
    cells = currentArea.celltab_set.all()
    area=[]
    part=[]
    for item in currentItems:
        part_dic = {'partId':item.area.part.id,'partCode':item.area.part.partCode}
        if part_dic not in part:
            part.append(part_dic)
        dic = {'areaId':item.area.id,'areaName':item.area.areaCode,'partId':item.area.part.id}
        area.append(dic)
    context={
        'damagePara':damagePara,
        'part':part,
        'area':area,
        'currentPlan':currentPlan,
        'currentArea':currentArea,
        'cells':cells
    }
    return render(request, 'evaluationManagement/damage/damageStat.html',context)

def changeSelect(request,type):
    # ret = {'status': False, 'message': '', 'data': None}
    data = []
    if request.method=='POST':
        post_data = request.POST.get('post_data', None)
        post_data_dict = json.loads(post_data)
        if type=='part':
            partId = post_data_dict['partId']
            currentPart = PartTab.objects.get(id=partId)
            areas = currentPart.areatab_set.all()
            for item in areas:
                dic={'id':item.id,'areaCode':item.areaCode}
                data.append(dic)
        if type=='area':
            areaId = post_data_dict['areaId']
            currentArea = AreaTab.objects.get(id=areaId)
            cells = currentArea.celltab_set.all()
            for item in cells:
                dic={'id':item.id,'cellCode':item.cellCode}
                data.append(dic)
        ret_str = json.dumps(data)
        return HttpResponse(ret_str)

def getPicData(request):
    ret = {'status': False, 'message': '', 'data': None}
    if request.method == 'POST':
        try:
            post_data = request.POST.get('post_data', None)
            post_data_dict = json.loads(post_data)
            damageId = post_data_dict['damageId']
            if post_data_dict['partId']=='':

                if damageId=='':
                    data = damageData.objects.filter(
                        surveyPlan_id=post_data_dict['PlanCode']
                    )
                else:
                    data = damageData.objects.filter(
                        surveyPlan_id=post_data_dict['PlanCode'],
                        damageType=int(post_data_dict['damageId'])
                    )
            else:
                if post_data_dict['areaId']=='':#
                    currentPart = PartTab.objects.get(id=post_data_dict['partId'])
                    areas = currentPart.areatab_set.all()
                    areaIds = []
                    for item in areas:
                        areaIds.append(item.id)
                    if damageId == '':
                        data = damageData.objects.filter(
                            surveyPlan_id=post_data_dict['PlanCode'],
                            area_id__in=areaIds
                        )
                    else:
                        data = damageData.objects.filter(
                            surveyPlan_id=post_data_dict['PlanCode'],
                            area_id__in=areaIds,
                            damageType=int(post_data_dict['damageId'])
                        )

                else:  # 指定区域
                    if post_data_dict['cellId']=='':#
                        area_id = int(post_data_dict['areaId'])
                        currentArea = AreaTab.objects.get(id=area_id)
                        cells = currentArea.celltab_set.all()
                        cellCodes = []
                        for item in cells:
                            cellCodes.append(item.getDisplayCellCode())
                        if damageId == '':
                            data = damageData.objects.filter(
                                surveyPlan_id=post_data_dict['PlanCode'],
                                area_id=area_id,
                                cell__in =cellCodes
                            )
                        else:
                            data = damageData.objects.filter(
                                surveyPlan_id=post_data_dict['PlanCode'],
                                area_id=area_id,
                                cell__in=cellCodes,
                                damageType=int(post_data_dict['damageId'])
                            )
                    else:
                        cell_code = post_data_dict['cellId']
                        if damageId == '':
                            data = damageData.objects.filter(surveyPlan_id=post_data_dict['PlanCode'],area_id=int(post_data_dict['areaId']),cell =cell_code)
                        else:
                            data = damageData.objects.filter(
                                surveyPlan_id=post_data_dict['PlanCode'],
                                area_id=int(post_data_dict['areaId']),
                                cell=cell_code,
                                damageType=int(post_data_dict['damageId'])
                            )
            datas = data.order_by('damageType').values("damageType").annotate(
                            sum_damageType=Count('damageType')
                        ).values('damageType', 'sum_damageType')
            data_=[]
            for item in datas:
                currentPara = parameterTab.objects.get(parameterType='damageType',parameterCode=item['damageType'])
                dic={'parameterName':currentPara.parameterName,'count':item['sum_damageType']}
                data_.append(dic)
            ret['data']=data_
        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'evaluationManagement/damage/damageStat.html')

def showDamageData(request,surveyPlanCode,areaId):
    currentPlan = surveyPlan.objects.get(surveyPlanCode=surveyPlanCode)
    currentArea = AreaTab.objects.get(id=areaId)
    AssessmentItems = assessmentItems.objects.get(surveyPlan=currentPlan,area=currentArea)
    # currentItem = assessmentItems.objects.filter()
    currentCom = structureComposition.objects.filter(structureCode=currentArea.structCode).first()
    if AssessmentItems.assessmentItem1_sureFlag=='' or AssessmentItems.assessmentItem1_sureFlag=='0':
        context = {
            'currentPlan': currentPlan,
            'currentArea': currentArea,
        }
        return render(request, 'evaluationManagement/damage/damageData_sureOper.html',context)
    else:
        damageDatas = damageData.objects.filter(surveyPlan=currentPlan, area=currentArea)
        data = []
        for item in damageDatas:
            # extra_str = '&nbsp;<span class="layui-badge-dot layui-bg-blue"></span>' if item.diseasephoto!='' else ''
            item = {"cellName": item.cell, "damageType": strTrans.transforDiseaseType(item.damageType),
                    "damageDegree": item.damageDegree,
                    "damageNumber": str(item.damageNumber), "unit": item.damageUnit,
                    "plateRow": item.palteRow, "plateCol": item.palteCol, "plateX": item.palteX,
                    "plateY": item.palteY, "diseasephoto": item.diseasephoto}
            #  这里 字段拼写与数据库不一致
            data.append(item)
        context = {
            'currentPlan': currentPlan,
            'currentArea': currentArea,
            'AssessmentItems': AssessmentItems,
            'currentCom':currentCom,
            'data':data
        }
        return render(request, 'evaluationManagement/damage/damageData.html', context)

def sureData(request):
    ret = {'status': False, 'message': '', 'data': None}
    if request.method == 'POST':
        try:
            post_data = request.POST.get('post_data', None)
            post_data_dict = json.loads(post_data)
            if post_data_dict['date'] == '' or post_data_dict['oper']=='':
                ret['message'] = '请将表单填写完整。'
            else:
                currentPlan = surveyPlan.objects.get(surveyPlanCode=post_data_dict['planCode'])
                currentArea = AreaTab.objects.get(id=post_data_dict['areaId'])
                assessmentItems.objects.filter(surveyPlan=currentPlan,area=currentArea)\
                    .update(assessmentItem1_sureFlag='1',Date_1=post_data_dict['date'],oper_1=post_data_dict['oper'])
                datas = damageData_ls.objects.filter(surveyPlan=currentPlan,area=currentArea)
                SH1=[]
                SH2=[]
                for item in datas:
                    damageData.objects.create(
                        surveyPlan=currentPlan,
                        area = currentArea,
                        cell = item.cell,
                        damageType = item.damageType,
                        damageDegree = item.damageDegree,
                        damageNumber = item.damageNumber,
                        damageUnit = item.damageUnit,
                        palteRow = item.palteRow,
                        palteCol = item.palteCol,
                        palteX = item.palteX,
                        palteY = item.palteY,
                        diseasephoto = item.diseasephoto
                    )
                    SH1.append(int(item.damageType))
                    SH2.append(item.damageDegree)
                # 计算PCI
                cellNum = cellTab.objects.filter(area=currentArea).count()
                [y, yy] = PCIcal.yangzheng(SH1, SH2, cellNum,round(cellNum * 400 / 25, 0))
                level = getLevel(y)
                PCI_result_area.objects.create(
                    surveyPlan=currentPlan,
                    area = currentArea,
                    areaPCI = y,
                    level = level
                )
                ret['message'] = '保存成功。'
                ret['status'] = True
        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'baseData/damageData_sureOper.html')

def getLevel(y):
    if y >= 85:
        level = '优'
    if y >= 70 and y < 85:
        level = '良'
    if y >= 55 and y < 70:
        level = '中'
    if y >= 40 and y < 55:
        level = '次'
    if y < 40:
        level = '差'
    return level


def uploadDamageData(request,surveyPlanCode,areaId):
    ret={'flag':True,'message':''}
    currentPlan = surveyPlan.objects.get(surveyPlanCode=surveyPlanCode)
    currentArea = AreaTab.objects.get(id=areaId)
    damageData_ls.objects.filter(area=currentArea, surveyPlan=currentPlan).delete()
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    if 'POST' == request.method:
        try:
            reqfile = request.FILES.get("file")
            filename = reqfile.name
            pathdir = os.path.join(settings.MEDIA_ROOT, 'damageData',surveyPlanCode,currentArea.areaCode).replace('\\','/')
            # pathRela = os.path.join('damageData',surveyPlanCode,currentArea.areaCode).replace('\\','/')
            dest = os.path.join(settings.MEDIA_ROOT, 'damageData',surveyPlanCode,currentArea.areaCode,request.user.username+current_time+filename[filename.find('.'):]).replace('\\','/')

            if not os.path.exists(pathdir):
                os.makedirs(pathdir)

            with open(dest, "wb") as destination:
                for chunk in reqfile.chunks():
                    destination.write(chunk)

            wb = xlrd.open_workbook(dest)  # 关键点在于这里
            [dataList,firstcol] = xlrd_read_excel.excel_table_byindex(wb, 7, 0)


            [flag,meg]=checkData(dataList)
            currentAirport_id = request.COOKIES.get('currentAirportId')
            currentAirport = airport_baseData.objects.get(id=currentAirport_id)

            if flag:
                [Data, reader, areaCode] = [firstcol[1].strip().lstrip().rstrip(),
                                            firstcol[4].strip().lstrip().rstrip(),
                                            firstcol[6].strip().lstrip().rstrip()]
                if areaCode == currentArea.getDisplayAreaCode():
                    if dataList.__len__() > 0:
                        count = 0
                        for i in range(0, dataList.__len__()):
                            try:
                                currentCell = cellTab.objects.get(cellCode=dataList[i].get('单元名称'))
                                cell = currentCell.getDisplayCellCode()


                                
                                damageNumber = dataList[i].get('损坏量(无需带单位)'),
                                if damageNumber in ['1', '6']:
                                    Unit = 'm'
                                elif damageNumber in ['8', '11']:
                                    Unit = '处'
                                else:
                                    Unit = 'm&sup2;'
                                # TODO 需要判断导入文件时，单元是否存在
                                damageData_ls.objects.create(
                                    area=currentArea,
                                    cell=cell,
                                    damageType=int(dataList[i].get('损坏类型')),
                                    damageDegree=dataList[i].get('损坏程度'),
                                    damageNumber=damageNumber[0],
                                    damageUnit=Unit,
                                    palteRow=str(int(dataList[i].get('行编号'))),
                                    palteCol=str(int(dataList[i].get('列编号'))),
                                    palteX='',
                                    palteY='',
                                    diseasephoto='',
                                    surveyPlan=currentPlan
                                )
                            except Exception as e:
                                count+=1
                                continue
                        ret['message'] = '文件导入成功' if count==0 else '过滤掉非本区域的单元共'+str(count)+'条'

                else:
                    ret['message'] = '文件所属区域与当前不符，请检查。'
                    ret['flag'] = False
                    os.remove(dest)
            else:
                ret['message'] = meg
                ret['flag'] = False
                os.remove(dest)

        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)

def checkData(dataList):
    message = "文件导入成功！"
    for i in range(0, dataList.__len__()):
        damageDegree_TRUE = ['L','M','H','N']
        damageValue = dataList[i].get('损坏量(无需带单位)')
        damageType = dataList[i].get('损坏类型')
        damageDegree = dataList[i].get('损坏程度')
        rowNum = dataList[i].get('行编号')
        colNum = dataList[i].get('列编号')
        cellCode = dataList[i].get('单元名称')
        if not numUtil.is_number(damageValue):
            message = '损坏量为数字，无需附带单位。<br\>[当前第' + str(
                i + 1) + '行 损坏量数据为<' + damageValue + '>]'
            return False, message
        if not numUtil.is_number(damageType):
            message = '损坏类型应为上述对应数字。<br\>[当前第' + str(
                i + 1) + '行 损坏量数据为<' + damageType + '>]'
            return False, message
        elif int(damageType)>15 and int(damageType)<1:
            message = '损坏类型不可超过1-15。<br\>[当前第' + str(
                i + 1) + '行 损坏量数据为<' + damageType + '>]'
            return False, message
        if damageDegree not in damageDegree_TRUE:
            message = '损坏程度应为L、M、H、N中选其一。<br\>[当前第' + str(
                i + 1) + '行 损坏量数据为<' + damageDegree + '>]'
            return False, message
        if (not numUtil.is_number(rowNum)) or  (not numUtil.is_number(rowNum)) or (not numUtil.is_number(colNum)) or \
                (not numUtil.is_number(colNum)):
            message = '行列编号应为数字。<br\>[当前第' + str(
                i + 1) + '行 行列编号为<' + rowNum+','+ colNum + '>]'
            return False, message
        if cellCode is None or cellCode=='':
            message = '请查询是否五单元编号列或单元编号为空。<br\>'
            return False, message
    return True, message

def searchDamageData(request,surveyPlanCode,areaId):
    ret = {"code": 0, "msg": "", "count": None, "data": None}
    if request.method == 'POST':
        limit = request.POST['limit']
        page = request.POST['page']
        searchStr =  request.POST.get('searchStr', '')
        currentPlan = surveyPlan.objects.get(surveyPlanCode=surveyPlanCode)
        currentArea = AreaTab.objects.get(id=areaId)

        damageDatas_ls = damageData_ls.objects.filter(surveyPlan=currentPlan,area=currentArea,cell__contains=searchStr)
        data = []
        for item in damageDatas_ls:
            # extra_str = '&nbsp;<span class="layui-badge-dot layui-bg-blue"></span>' if item.diseasephoto!='' else ''
            item = {"id":item.id,"cellName": item.cell, "damageType": strTrans.transforDiseaseType(item.damageType), "damageDegree": item.damageDegree,
                    "damageNumber": str(item.damageNumber), "unit": item.damageUnit,
                    "plateRow": item.palteRow, "plateCol": item.palteCol, "plateX": item.palteX,
                    "plateY": item.palteY,"diseasephoto":item.diseasephoto}
            #  这里 字段拼写与数据库不一致
            data.append(item)
        count = data.__len__()
        [currentpage, maxpage, minpage, maxpage] = commUtil.GetYeMa(page, limit, count)
        ret['count'] = count
        ret['data'] = data[minpage - 1:maxpage]
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'evaluationManagement/damage/damageData_sureOper.html')

def uploadPic(request,surveyPlanCode,areaId):
    return render(request, 'evaluationManagement/damage/uploadpicDialog.html',locals())

def receivePic(request,surveyPlanCode,areaId):
    ret = {"code": 0, "msg": "", "count": None, "data": None}
    currentArea = AreaTab.objects.get(id=areaId)
    curentPlan = surveyPlan.objects.get(surveyPlanCode=surveyPlanCode)
    if request.method=='POST':
        reqfile = request.FILES.get("file")
        filename = reqfile.name
        pathdir = os.path.join(settings.MEDIA_ROOT, 'damageData_pic', surveyPlanCode,currentArea.areaCode).replace('\\', '/')
        pathRela = os.path.join('damageData_pic',surveyPlanCode,currentArea.areaCode,filename).replace('\\','/')
        dest = os.path.join(settings.MEDIA_ROOT, 'damageData_pic', surveyPlanCode,currentArea.areaCode,filename).replace('\\', '/')



        if not os.path.exists(pathdir):
            os.makedirs(pathdir)

        with open(dest, "wb") as destination:
            for chunk in reqfile.chunks():
                destination.write(chunk)

        fileName_noSuffix = filename[0:filename.find('.')]
        info = fileName_noSuffix.split('_')
        if len(info)==3:
            [cell,rowNo,colNo]=info
            data_temp = damageData_ls.objects.filter(surveyPlan=curentPlan,area=currentArea,cell=cell,palteRow=rowNo,palteCol=colNo)
            if data_temp:
                data_temp.update(diseasephoto=pathRela)
            else:
                ret['code'] = 1
                ret['msg'] = '找不到匹配'
        else:
            ret['msg'] = '无匹配文件'
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'evaluationManagement/damage/uploadpicDialog.html')

def lookAllPic(request,surveyPlanCode,areaId):
    ret = {"title": '损害图片', "start": 0,  "data": []}
    currentArea = AreaTab.objects.get(id=areaId)
    curentPlan = surveyPlan.objects.get(surveyPlanCode=surveyPlanCode)
    if request.method == 'POST':
        pathdir = os.path.join(settings.MEDIA_ROOT, 'damageData_pic', surveyPlanCode, currentArea.getDisplayAreaCode()).replace(
            '\\', '/')
        static_root = os.path.join('/static', 'damageData_pic', surveyPlanCode, currentArea.getDisplayAreaCode()).replace(
            '\\', '/')
        list = os.listdir(pathdir)
        for i in range(0, len(list)):
            path = os.path.join(static_root, list[i]).replace(
            '\\', '/')
            dic = {'alt':list[i],'src':path}
            ret['data'].append(dic)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)

def delDamageData(request):
    ret = {'status': False, 'message': '', 'data': None}
    if request.method == 'POST':
        post_data = request.POST.get('post_data', None)
        post_data_dict = json.loads(post_data)
        id = post_data_dict['id']
        damageDatas_ls = damageData_ls.objects.get(id=id).delete()
        ret['status']=True
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'evaluationManagement/damage/damageData_sureOper.html')

def downloadStaticFile(request,fileType):
    if fileType=='damageData':
        filename = '损坏数据导入格式模板'
    if fileType=='deflectData':
        filename = '板弯沉数据导入格式模板'
    if fileType=='planenessData':
        filename = '平整度IRI模板'
    if fileType=='section':
        filename = '地铁结构信息导入格式'
    if fileType=='linetype':
        filename = '地铁线形信息导入格式'
    def file_iterator(file_name):
        with open(file_name,'rb') as f:
            while True:
                c = f.read()
                if c:
                    yield c
                else:
                    break

    filepath = 'upload/Temple_forExcel/'+filename+'.xlsx'
    response = StreamingHttpResponse(file_iterator(filepath))
    response['Content-Type'] = 'application/octet-stream'
    agent = request.META.get('HTTP_USER_AGENT')
    if agent.upper().find("MSIE") != -1:
        response['Content-Disposition'] ="attachment; filename={0}".format(filename + '.xlsx').encode('gbk').decode('latin-1')
    elif agent.upper().find("EDGE") != -1:
        response['Content-Disposition'] = "attachment; filename={0}".format(filename+'.xlsx').encode('gb2312')
    else:
        response['Content-Disposition'] = "attachment; filename={0}".format(filename + '.xlsx').encode('utf8')
    return response

def pciCalData(request,surveyPlanCode,areaId):
    currentPlan = surveyPlan.objects.get(surveyPlanCode=surveyPlanCode)
    currentArea = AreaTab.objects.get(id=areaId)
    currentItems = assessmentItems.objects.get(area=currentArea,surveyPlan=currentPlan)
    data=[]
    if currentItems.assessmentItem1_sureFlag=='1':
        pci_res = PCI_result_area.objects.filter(area=currentArea,surveyPlan=currentPlan)

        for item in pci_res:
            # extra_str = '&nbsp;<span class="layui-badge-dot layui-bg-blue"></span>' if item.diseasephoto!='' else ''
            item = {"areaName": item.area.getDisplayAreaCode(), "area_PCI": str(item.areaPCI),
                    "area_SCI": str(item.areaSCI),
                    "min_cell_PCI": '', "max_cell_PCI": '',
                    "level": item.level, "PCI_coefficient": str(item.PCI_coefficient), "Date": currentPlan.endTime}
            #  这里 字段拼写与数据库不一致
            data.append(item)
    # currentItem = assessmentItems.objects.filter()
    context={
        'currentPlan':currentPlan,
        'currentArea':currentArea,
        'data':data
    }
    return render(request, 'evaluationManagement/damage/pciCal.html',context)

def initdamageStatisticsFrame(request):
    allOperArea = assessmentItems.objects.filter(assessmentItem__contains='1').order_by('-surveyPlan_id','area_id')#  1 指的是损坏数据
    allPlan = surveyPlan.objects.filter(surveyPlanCode__in=allOperArea.values('surveyPlan_id')).order_by('-surveyPlanCode')
    firstPlan = allPlan.first()
    firstOperArea = allOperArea.first()
    if firstPlan:
        context={
            'allPlan':allPlan,
            'allOperArea':allOperArea,
            'firstPlan':firstPlan,
            'firstOperArea':firstOperArea,
        }
        return render(request, 'evaluationManagement/damage/initdamageStatisticsFrame.html',context)
    return HttpResponse("请先添加计划。")



# # 弯沉记录与评价
def initDeflectionRecordsAndEvaluation(request):
    allOperArea = assessmentItems.objects.filter(assessmentItem__contains='2').order_by('-surveyPlan_id','area_id')#  1 指的是损坏数据
    allPlan = surveyPlan.objects.filter(surveyPlanCode__in=allOperArea.values('surveyPlan_id')).order_by('-surveyPlanCode')
    firstPlan = allPlan.first()
    firstOperArea = allOperArea.first()
    context={
        'allPlan':allPlan,
        'allOperArea':allOperArea,
        'firstPlan':firstPlan,
        'firstOperArea':firstOperArea,
    }
    return render(request, 'evaluationManagement/deflection/initDeflectionFrame.html',context)

# 根据状态  展示待确认数据  或  已确认数据
def deflectionData(request,surveyPlanCode,areaId):
    currentPlan = surveyPlan.objects.get(surveyPlanCode=surveyPlanCode)
    currentArea = AreaTab.objects.get(id=areaId)
    AssessmentItems = assessmentItems.objects.get(surveyPlan=currentPlan,area=currentArea)

    if AssessmentItems.assessmentItem2_sureFlag=='' or AssessmentItems.assessmentItem2_sureFlag=='0':
        context = {
            'currentPlan': currentPlan,
            'currentArea': currentArea,
        }
        return render(request, 'evaluationManagement/deflection/deflectData_sureOper.html',context)
    if AssessmentItems.assessmentItem2_sureFlag=='1':
        deflectDatas = deflectData.objects.filter(surveyPlan=currentPlan, area=currentArea)
        currentCom = structureComposition.objects.filter(structureCode=currentArea.structCode).first()
        data = []
        for item in deflectDatas:
            # extra_str = '&nbsp;<span class="layui-badge-dot layui-bg-blue"></span>' if item.diseasephoto!='' else ''
            item = {"id": item.id, "plateCode": item.plateCode,
                    "loadPosition": item.loadPosition,
                    "D1": str(item.D1), "D2": str(item.D2), "D3": str(item.D3), "D4": str(item.D4), "D5": str(item.D5),
                    "D6": str(item.D6), "D7": str(item.D7), "D8": str(item.D8), "D9": str(item.D9),
                    "load": str(item.load) }
            #  这里 字段拼写与数据库不一致
            data.append(item)
        context = {
            'currentPlan': currentPlan,
            'currentArea': currentArea,
            'AssessmentItems': AssessmentItems,
            'currentCom':currentCom,
            'data': data
        }
        return render(request, 'evaluationManagement/deflection/deflectData.html',context)


def sureDeflectData(request):
    ret = {'status': False, 'message': '', 'data': None}
    if request.method == 'POST':
        try:
            post_data = request.POST.get('post_data', None)
            post_data_dict = json.loads(post_data)
            if post_data_dict['date'] == '' or post_data_dict['oper'] == '' or post_data_dict['surfaceTemperature'] == '' or post_data_dict['bearingPlateRadius'] == '' or post_data_dict['distance'] == '':
                ret['message'] = '请将表单填写完整。'
            else:
                currentPlan = surveyPlan.objects.get(surveyPlanCode=post_data_dict['planCode'])
                currentArea = AreaTab.objects.get(id=post_data_dict['areaId'])
                assessmentItems.objects.filter(surveyPlan=currentPlan, area=currentArea) \
                    .update(assessmentItem2_sureFlag='1', Date_2=post_data_dict['date'], oper_2=post_data_dict['oper'],
                            suface_Tem_2=post_data_dict['surfaceTemperature'],bearingplate_radius_2=post_data_dict['bearingPlateRadius'],
                            distance_2=post_data_dict['distance']
                            )
                datas = deflectData_ls.objects.filter(surveyPlan=currentPlan, area=currentArea)
                SH1 = []
                SH2 = []
                for item in datas:
                    deflectData.objects.create(
                        surveyPlan=currentPlan,
                        area = currentArea,
                        plateCode = item.plateCode,
                        loadPosition = item.loadPosition,
                        D1 = item.D1,
                        D2 = item.D2,
                        D3 = item.D3,
                        D4 = item.D4,
                        D5 = item.D5,
                        D6 = item.D6,
                        D7 = item.D7,
                        D8 = item.D8,
                        D9 = item.D9,
                        load = item.load,
                    )
                    # TODO 计算各类参数
                # 计算接缝性能
                cursor = connection.cursor()
                cursor.execute('''
                        SELECT
                            AVG(maxD3_D12),AVG(great),AVG(mid),AVG(ci),AVG(cha)
                        FROM(
                        SELECT
                            D3 / GREATEST(D1, D2) AS maxD3_D12,
                            case when D3 / GREATEST(D1, D2)> 0.8 then 1 else 0 end as great,
                            case when D3 / GREATEST(D1, D2)<= 0.8 and D3 / GREATEST(D1, D2) >= 0.56 then 1 else 0 end as mid,
                            case when D3 / GREATEST(D1, D2)<= 0.55 and D3 / GREATEST(D1, D2) >= 0.31 then 1 else 0 end as ci,
                            case when D3 / GREATEST(D1, D2)< 0.31 then 1 else 0 end as cha,
                            D3 / D1,
                            D3 / D2
                        FROM
                            evaluationmanagement_deflectdata
                        WHERE
                            surveyPlan_id = %s
                        AND area_id = %s
                        AND loadPosition = '板边'
                        )x
                        ''', [currentPlan.surveyPlanCode,currentArea.id])
                JoinSevaluation = cursor.fetchall()
                cursor.execute('''
                                select
                                    avg_1_3,
                                    avg_1_max_3,
                                    avg_1_min_3,
                                    avg_2_3,
                                    avg_2_max_3,
                                    avg_2_min_3,
                                    rate_1,
                                    rate_2,
                                    rate_3,
                                    rate_1_new,
                                    rate_2_new,
                                    rate_3_new,
                                    a.area_id,
                                    c.areaCode
                                from (
                                    SELECT
                                            avg(D1_3) AS avg_1_3,
                                            MAX(D1_3) AS avg_1_max_3,
                                            MIN(D1_3) AS avg_1_min_3,
                                            avg(D2_3) AS avg_2_3,
                                            MAX(D2_3) AS avg_2_max_3,
                                            MIN(D2_3) AS avg_2_min_3,
                                            area_id
                                    FROM
                                            (
                                                    SELECT
                                                            sum(D1_1) / sum(D1_3) AS D1_3,
                                                            sum(D1_2) / sum(D1_3) AS D2_3,
                                                            area_id
                                                    FROM
                                                            (
                                                                    select
                                                                                    plateCode,
                                                                                    case when loadPosition= '板边' then D1 else 0 end as D1_1,
                                                                                    case when loadPosition= '板角' then D1 else 0 end as D1_2,
                                                                                    case when loadPosition= '板中' then D1 else 0 end as D1_3,
                                                                                    area_id
                                                                    from(
                                                                                    SELECT
                                                                                        plateCode,loadPosition,case when loadPosition= '板边' then GREATEST(D2,D1) else D1 end as D1,area_id
                                                                                    FROM
                                                                                        evaluationmanagement_deflectdata
                                                                                    WHERE
                                                                                        surveyPlan_id = %s
                                                                                    AND area_id = %s
                                                                    ) x
                                    ) y
                                    GROUP BY
                                            plateCode,
                                            area_id
                                    ) z
                                    GROUP BY
                                            area_id
                              ) a left join (
                                    select
                                            COALESCE(sum(case when deflection='板边脱空' then 1 when deflection='脱空' then 1 else 0 end)/count(deflection),0) as rate_1,
                                            COALESCE(sum(case when deflection='板角脱空' then 1 when deflection='脱空' then 1 else 0 end)/count(deflection),0) as rate_2,
                                            COALESCE(sum(case when deflection!='不脱空' then 1  end)/count(deflection),0) as rate_3,
                                            COALESCE(sum(case when deflection_new='板边脱空' then 1 when deflection='脱空' then 1 else 0 end)/count(deflection),0) as rate_1_new,
                                            COALESCE(sum(case when deflection_new='板角脱空' then 1 when deflection='脱空' then 1 else 0 end)/count(deflection),0) as rate_2_new,
                                            COALESCE(sum(case when deflection_new!='不脱空' then 1  end)/count(deflection),0) as rate_3_new,
                                            area_id
                                    from (
                                    select  plateCode,
                                                                    local_1_3,
                                                                    local_2_3,
                                                                    case when local_1_3<=2 and  local_2_3<=3 then '不脱空'
                                                                                     when local_1_3>2 and  local_2_3<=3 then '板边脱空'
                                                                                     when local_1_3<=2 and  local_2_3>3 then '板角脱空'
                                                                                     else '脱空' end as deflection,
                                                                    case  when maxD3_D12>0.56
                                                                          then
                                                                                    case when local_1_3<=2 and  local_2_3<=3 then '不脱空'
                                                                                             when local_1_3>2 and  local_2_3<=3 then '板边脱空'
                                                                                             when local_1_3<=2 and  local_2_3>3 then '板角脱空'
                                                                                             else '脱空' end
                                                                          when maxD3_D12<=0.56
                                                                          then
                                                                                    case when local_1_3<=3.5 and  local_2_3<=6 then '不脱空'
                                                                                             when local_1_3>3.5 and  local_2_3<=6 then '板边脱空'
                                                                                             when local_1_3<=3.5 and  local_2_3>6 then '板角脱空'
                                                                                             else '脱空' end
                                                                    end as deflection_new,
                                                                    area_id
                                                                    from(
                                                                    select  plateCode,
                                                                                 COALESCE(sum(case when loadPosition='板边' then D1 end),0)/sum(case when loadPosition='板中' then D1 end) as local_1_3,
                                                                                COALESCE(sum(case when loadPosition='板角' then D1 end),0) /sum(case when loadPosition='板中' then D1 end) as local_2_3,
                                                                                sum(maxD3_D12) as maxD3_D12,
                                                                                area_id
                                                                    from (
                                                                        SELECT
                                                                            plateCode,loadPosition,case when loadPosition= '板边' then GREATEST(D2,D1) else D1 end as D1,
                                                                            case when loadPosition= '板边' then D3 / GREATEST(D1, D2) else 0 end AS maxD3_D12,area_id
                                                                        FROM
                                                                            evaluationmanagement_deflectdata
                                                                        WHERE
                                                                            surveyPlan_id = %s
                                                                        AND area_id = %s
                                                                    ) x

                                                                            GROUP BY area_id,plateCode
                                                                            ) y
                                    ) z
                                            GROUP BY area_id
                                    ) b on a.area_id=b.area_id
                                    left join main_areatab c on a.area_id=c.id
              ''',[currentPlan.surveyPlanCode,currentArea.id,currentPlan.surveyPlanCode,currentArea.id])
                VoidSevaluation = cursor.fetchall()
                cursor.close()
                for item in JoinSevaluation:
                    join_result_area.objects.create(
                        surveyPlan=currentPlan,
                        area = currentArea,
                        avg = round(item[0]*100,2),
                        level_good = round(item[1]*100,2),
                        level_mid = round(item[2]*100,2),
                        level_ci = round(item[3]*100,2),
                        level_cha = round(item[4]*100,2),
                    )
                for item in VoidSevaluation:
                    void_result_area.objects.create(
                        surveyPlan=currentPlan,
                        area = currentArea,
                        bian_zhong_avg = round(item[0],2),
                        bian_zhong_max = round(item[1],2),
                        bian_zhong_min = round(item[2],2),
                        bian_radio_2_3 = round(item[6]*100,2),
                        bian_radio_3_6 = round(item[9]*100,2),
                        jiao_zhong_avg = round(item[3],2),
                        jiao_zhong_max = round(item[4],2),
                        jiao_zhong_min = round(item[5],2),
                        jiao_radio_2_3 = round(item[7]*100,2),
                        jiao_radio_3_6 = round(item[10]*100,2),
                        radio_2_3 = round(item[8]*100,2),
                        radio_3_6 = round(item[11]*100,2),
                    )

                ret['message'] = '保存成功。'
                ret['status'] = True
        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'evaluationManagement/deflection/deflectData_sureOper.html')

def editDeflectData(request):
    ret = {'status': False, 'message': '', 'data': None}
    if request.method == 'POST':
        post_data = request.POST.get('post_data', None)
        post_data_dict = json.loads(post_data)

        editfield = post_data_dict['editfield']
        value = post_data_dict['value']
        id = post_data_dict['id']
        deflectDatas_ls = deflectData_ls.objects.get(id=id)
        if deflectDatas_ls:
            try:
                setattr(deflectDatas_ls,editfield,round(float(value),1))
                deflectDatas_ls.save()
            except Exception as e:
                ret['message'] = str(e)
            ret['status']=True
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'evaluationManagement/deflection/deflectData_sureOper.html')

def delDeflectData(request):
    ret = {'status': False, 'message': '', 'data': None}
    if request.method == 'POST':
        post_data = request.POST.get('post_data', None)
        post_data_dict = json.loads(post_data)
        id = post_data_dict['id']
        deflectDatas_ls = deflectData_ls.objects.get(id=id).delete()
        ret['status']=True
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'evaluationManagement/deflection/deflectData_sureOper.html')

def searchDeflectData(request, surveyPlanCode, areaId):
    ret = {"code": 0, "msg": "", "count": None, "data": None}
    if request.method == 'POST':
        limit = request.POST['limit']
        page = request.POST['page']
        searchStr = request.POST.get('searchStr', '')
        currentPlan = surveyPlan.objects.get(surveyPlanCode=surveyPlanCode)
        currentArea = AreaTab.objects.get(id=areaId)

        deflectDatas_ls = deflectData_ls.objects.filter(surveyPlan=currentPlan, area=currentArea,
                                                        plateCode__contains=searchStr)
        data = []
        for item in deflectDatas_ls:
            item = {"id": item.id, "plateCode": item.plateCode,
                    "loadPosition": item.loadPosition,
                    "D1": item.D1,"D2": item.D2,"D3": item.D3,"D4": item.D4,"D5": item.D5,"D6": item.D6,
                    "D7": item.D7,"D8": item.D8,"D9": item.D9, "load": item.load}
            data.append(item)
        count = data.__len__()
        [currentpage, maxpage, minpage, maxpage] = commUtil.GetYeMa(page, limit, count)
        ret['count'] = count
        ret['data'] = data[minpage - 1:maxpage]
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'evaluationManagement/deflection/deflectData_sureOper.html')

def deflectData_analy(request,surveyPlanCode,areaId):
    currentPlan = surveyPlan.objects.get(surveyPlanCode=surveyPlanCode)
    currentArea = AreaTab.objects.get(id=areaId)

    # 接缝评价结果
    join_data = join_result_area.objects.filter(surveyPlan=currentPlan,area=currentArea)
    join_json=[]
    for item in join_data:
        join_json.append({'areaName':item.area.getDisplayAreaCode(),'level_avg':str(item.avg)+'%',
                          'level_good': str(item.level_good)+'%', 'level_mid': str(item.level_mid)+'%',
                          'level_ci': str(item.level_ci)+'%', 'level_cha': str(item.level_cha)+'%'})
    # 脱空结果
    void_data = void_result_area.objects.filter(surveyPlan=currentPlan,area=currentArea)
    void_json = []
    for item in void_data:
        void_json.append({
            'areaName':item.area.getDisplayAreaCode(),'bian_zhong_avg':str(item.bian_zhong_avg),'bian_zhong_max':str(item.bian_zhong_max),
            'bian_zhong_min': str(item.bian_zhong_min), 'jiao_zhong_avg': str(item.jiao_zhong_avg), 'jiao_zhong_max': str(item.jiao_zhong_max),
            'jiao_zhong_min':str(item.jiao_zhong_min),'bian_radio_2_3':str(item.bian_radio_2_3)+'%','jiao_radio_2_3':str(item.jiao_radio_2_3)+'%',
            'radio_2_3':str(item.radio_2_3)+'%','bian_radio_3_6':str(item.bian_radio_3_6)+'%','jiao_radio_3_6':str(item.jiao_radio_3_6)+'%','radio_3_6':str(item.radio_3_6)+'%'
        })
    # 脱空统计图
    void_chart_data_x = []
    void_chart_data_y = []
    join_chart_data_x = []
    join_chart_data_y = []
    chart_data = [void_chart_data_x,void_chart_data_y,join_chart_data_x,join_chart_data_y]
    for item in void_data:
        void_chart_data_x.append(item.area.getDisplayAreaCode())
        void_chart_data_y.append(str(item.radio_2_3))
    for item in join_data:
        join_chart_data_x.append(item.area.getDisplayAreaCode())
        join_chart_data_y.append(str(item.avg))

    context={
        'currentPlan':currentPlan,
        'currentArea':currentArea,
        'join_json':join_json,
        'void_json':void_json,
        'chart_data':chart_data
    }
    return render(request, 'evaluationManagement/deflection/deflectData_analy.html',context)

# 弯沉数据导入
def uploadDeflectData(request,surveyPlanCode,areaId):
    ret={'flag':True,'message':''}
    currentPlan = surveyPlan.objects.get(surveyPlanCode=surveyPlanCode)
    currentArea = AreaTab.objects.get(id=areaId)
    deflectData_ls.objects.filter(area=currentArea, surveyPlan=currentPlan).delete()
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    if 'POST' == request.method:
        try:
            reqfile = request.FILES.get("file")
            filename = reqfile.name
            pathdir = os.path.join(settings.MEDIA_ROOT, 'deflectData',surveyPlanCode,currentArea.areaCode).replace('\\','/')
            # pathRela = os.path.join('damageData',surveyPlanCode,currentArea.areaCode).replace('\\','/')
            dest = os.path.join(settings.MEDIA_ROOT, 'deflectData',surveyPlanCode,currentArea.areaCode,request.user.username+current_time+filename[filename.find('.'):]).replace('\\','/')

            if not os.path.exists(pathdir):
                os.makedirs(pathdir)

            with open(dest, "wb") as destination:
                for chunk in reqfile.chunks():
                    destination.write(chunk)

            wb = xlrd.open_workbook(dest)  # 关键点在于这里
            [dataList,firstcol] = xlrd_read_excel.excel_table_byindex(wb, 0, 0)


            [flag,meg]=checkDeflectData(dataList)
            if flag:
                if dataList.__len__() > 0:
                    for i in range(0, dataList.__len__()):
                        deflectData_ls.objects.create(
                            surveyPlan=currentPlan,
                            area = currentArea,
                            plateCode = dataList[i].get('板编号'),
                            loadPosition = dataList[i].get('荷位'),
                            D1 = dataList[i].get('D(1)'),
                            D2 = dataList[i].get('D(2)'),
                            D3 = dataList[i].get('D(3)'),
                            D4 = dataList[i].get('D(4)'),
                            D5 = dataList[i].get('D(5)'),
                            D6 = dataList[i].get('D(6)'),
                            D7 = dataList[i].get('D(7)'),
                            D8 = dataList[i].get('D(8)'),
                            D9 = dataList[i].get('D(9)'),
                            load = dataList[i].get('荷载/Kn')
                        )
            else:
                ret['message'] = meg
                ret['flag'] = False
                os.remove(dest)

        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)

def checkDeflectData(dataList):
    message = "文件导入成功！"
    for i in range(0, dataList.__len__()):
        loadPosition_TRUE = ['板边','板中','板角']
        plateCode = dataList[i].get('板编号')
        loadPosition = dataList[i].get('荷位')
        DData = [D1,D2,D3,D4,D5,D6,D7,D8,D9] = [dataList[i].get('D(1)'),dataList[i].get('D(2)'),
                                        dataList[i].get('D(3)'),dataList[i].get('D(4)'),
                                        dataList[i].get('D(5)'),dataList[i].get('D(6)'),
                                        dataList[i].get('D(7)'),dataList[i].get('D(8)'),
                                        dataList[i].get('D(9)'),]
        load = dataList[i].get('荷载/Kn')
        if not numUtil.is_all_number_Matrix(DData):
            message = '传感器数据应为数字。'
            return False, message
        if plateCode==None or plateCode=='':
            message = '板编号不能为空。'
            return False, message
        if loadPosition not in loadPosition_TRUE:
            message = '荷位应为[板边,板中,板角]中选其一。'
            return False, message
        if not numUtil.is_number(load):
            message = '荷载应为数字'
            return False, message
    return True, message


# # 平整度记录与评价
def initPlanenessRecordsAndEvaluation(request):
    allOperArea = assessmentItems.objects.filter(assessmentItem__contains='3').order_by('-surveyPlan_id','area_id')#  1 指的是损坏数据
    allPlan = surveyPlan.objects.filter(surveyPlanCode__in=allOperArea.values('surveyPlan_id')).order_by('-surveyPlanCode')
    firstPlan = allPlan.first()
    firstOperArea = allOperArea.first()

    # part = []
    # for operArea in allOperArea:
    #     dict = {'surveyPlanCode': operArea.surveyPlan.surveyPlanCode, 'part': operArea.area.part.airCode,
    #             'partId': operArea.area.part.id}
    #     if dict not in part:
    #         part.append(dict)
    context={
        'allPlan':allPlan,
        'allOperArea':allOperArea,
        'firstPlan':firstPlan,
        'firstOperArea':firstOperArea,
    }
    return render(request, 'evaluationManagement/planeness/initPlanenessFrame.html',context)

def showplanenessData(request,surveyPlanCode,partId):
    currentPlan = surveyPlan.objects.get(surveyPlanCode=surveyPlanCode)
    currentPart = PartTab.objects.get(id=partId)
    get_all_area = currentPart.areatab_set.all()
    AssessmentItems = assessmentItems.objects.filter(surveyPlan=currentPlan,area__in=get_all_area)
    flag=[]
    for item in AssessmentItems:
        flag.append(int(item.assessmentItem3_sureFlag))

    if sum(flag)==0:
        lineCodeSelect = planenessData_ls.objects.filter(surveyPlan=currentPlan,part=currentPart).values('lineCode').distinct()
        context = {
            'currentPlan': currentPlan,
            'currentPart':currentPart,
            'lineCodeSelect':lineCodeSelect
        }
        return render(request, 'evaluationManagement/planeness/planenessData_sureOper.html',context)
    if sum(flag)==AssessmentItems.__len__():
        planenessDatas = planenessData.objects.filter(surveyPlan=currentPlan, part=currentPart)
        data = []
        for item in planenessDatas:
            item = {"id": item.id, "lineCode": item.lineCode,
                    "stakeNo": str(int(item.stakeNo)),
                    "left_iri": str(item.left_iri), "left_variance": str(item.left_variance),
                    "right_iri": str(item.right_iri), "right_variance": str(item.right_variance), "iri_avg": str(item.iri_avg) }
            data.append(item)
        context = {
            'currentPlan': currentPlan,
            'AssessmentItems': AssessmentItems[0],
            'currentPart': currentPart,
            'data': data
        }
        return render(request, 'evaluationManagement/planeness/planenessData.html',context)

def uploadPlanenessData(request,surveyPlanCode,partId):
    ret={'flag':True,'message':''}
    currentPlan = surveyPlan.objects.get(surveyPlanCode=surveyPlanCode)
    currentPart = PartTab.objects.get(id=partId)
    planenessData_ls.objects.filter(part=currentPart, surveyPlan=currentPlan).delete()
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    if 'POST' == request.method:
        try:
            reqfile = request.FILES.get("file")
            filename = reqfile.name
            pathdir = os.path.join(settings.MEDIA_ROOT, 'planenessData',surveyPlanCode,currentPart.partCode).replace('\\','/')
            # pathRela = os.path.join('damageData',surveyPlanCode,currentArea.areaCode).replace('\\','/')
            dest = os.path.join(settings.MEDIA_ROOT, 'planenessData',surveyPlanCode,currentPart.partCode,request.user.username+current_time+filename[filename.find('.'):]).replace('\\','/')

            if not os.path.exists(pathdir):
                os.makedirs(pathdir)

            with open(dest, "wb") as destination:
                for chunk in reqfile.chunks():
                    destination.write(chunk)

            wb = xlrd.open_workbook(dest)  # 关键点在于这里
            # [dataList,firstcol] = xlrd_read_excel.excel_table_byindex(wb, 0, 0)
            table = wb.sheets()[0]
            nrows = table.nrows  # 行数
            ncols = table.ncols  # 列数
            colnames = table.row_values(1)  # 读取首行内容
            codeName = table.row_values(0)  # 读取首行内容
            for rownum in range(2, nrows):
                row = table.row_values(rownum)
                if row:
                    count = int((len(colnames)-1)/5)
                    for coun in range(0,count):
                        planenessData_ls.objects.create(
                                surveyPlan=currentPlan,
                                part = currentPart,
                                lineCode = codeName[coun*5+1],
                                stakeNo =  row[0],
                                left_iri = row[coun*5+2] if isFloat(row[coun*5+2]) else 0.0,
                                left_variance = row[coun*5+4] if isFloat(row[coun*5+4]) else 0.0,
                                right_iri = row[coun*5+3] if isFloat(row[coun*5+3]) else 0.0,
                                right_variance = row[coun*5+5] if isFloat(row[coun*5+5]) else 0.0,
                            )
        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)

def isFloat(a):
    isFloat=True
    try:
        float(a)
    except:
        isFloat = False
    return isFloat

def searchPlanenessData(request,surveyPlanCode,partId):
    ret = {"code": 0, "msg": "", "count": None, "data": None}
    if request.method == 'POST':
        limit = request.POST['limit']
        page = request.POST['page']
        searchStr = request.POST.get('searchStr', '')
        lineCode = request.POST.get('lineCode', '')
        currentPlan = surveyPlan.objects.get(surveyPlanCode=surveyPlanCode)
        currentPart = PartTab.objects.get(id=partId)

        planenessData = planenessData_ls.objects.filter(surveyPlan=currentPlan, part=currentPart,
                                                        stakeNo__contains=searchStr,lineCode__contains=lineCode)
        data = []
        for item in planenessData:
            zero_count = 0
            if item.left_iri==0:
                zero_count=zero_count+1
            if item.right_iri == 0:
                zero_count = zero_count + 1
            try:
                item = {"id": item.id, "lineCode": item.lineCode,
                        "stakeNo": str(int(item.stakeNo)),
                        "left_iri": str(item.left_iri) if item.left_iri!=0 else '-', "left_variance": str(item.left_variance) if item.left_variance!=0 else '-',
                        "right_iri": str(item.right_iri) if item.right_iri!=0 else '-',
                        "right_variance": str(item.right_variance) if item.right_variance!=0 else '-', "iri_avg": str(round((item.left_iri+item.right_iri)/zero_count,2))}
                data.append(item)
            except Exception as e:
                ret['msg'] = str(e)
        count = data.__len__()
        [currentpage, maxpage, minpage, maxpage] = commUtil.GetYeMa(page, limit, count)
        ret['count'] = count
        ret['data'] = data[minpage - 1:maxpage]
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'evaluationManagement/deflection/deflectData_sureOper.html')

def surePlanenessData(request):
    ret = {'status': False, 'message': '', 'data': None}
    if request.method == 'POST':
        try:
            post_data = request.POST.get('post_data', None)
            post_data_dict = json.loads(post_data)
            if post_data_dict['date'] == '' or post_data_dict['oper']=='' or post_data_dict['testDesc']==''or\
                            post_data_dict['samplingDistance']==''or post_data_dict['measuringLine_length']=='' :
                ret['message'] = '请将表单填写完整。'
            else:
                currentPlan = surveyPlan.objects.get(surveyPlanCode=post_data_dict['planCode'])
                currentPart = PartTab.objects.get(id=post_data_dict['partId'])
                operAreas = currentPart.areatab_set.all()
                assessmentItems.objects.filter(surveyPlan=currentPlan,area__in=operAreas)\
                    .update(assessmentItem3_sureFlag='1',Date_3=post_data_dict['date'],oper_3=post_data_dict['oper'],
                            measuringLine_length_3=post_data_dict['measuringLine_length'],samplingDistance_3=post_data_dict['samplingDistance'],
                            testDesc_3=post_data_dict['testDesc'])

                datas = planenessData_ls.objects.filter(surveyPlan=currentPlan,part=currentPart)
                for item in datas:
                    zero_count = 0
                    if item.left_iri == 0:
                        zero_count = zero_count + 1
                    if item.right_iri == 0:
                        zero_count = zero_count + 1
                    planenessData.objects.create(
                        surveyPlan=currentPlan,
                        part = currentPart,
                        lineCode=item.lineCode,
                        stakeNo = item.stakeNo,
                        left_iri = item.left_iri,
                        left_variance = item.left_variance,
                        right_iri = item.right_iri,
                        right_variance = item.right_variance,
                        iri_avg = round((item.left_iri + item.right_iri) / zero_count, 2)
                    )
                # 计算 IRI 评价结果
                cursor = connection.cursor()
                cursor.execute('''
                                select id,lineCode,avg_iri,
                                            round(variation_iri,2),
                                            case when avg_iri<2 then '好'
                                                        when avg_iri>=2 and avg_iri<=4 then '中'
                                                        when avg_iri>4 then '差'  end as pf

                                from (
                                SELECT
                                    b.id,
                                    lineCode,
                                    case when AVG(left_iri) =0 or AVG(right_iri)=0
                                                    then ROUND(AVG(left_iri)+AVG(right_iri), 2)
                                            ELSE ROUND((AVG(left_iri)+AVG(right_iri))/2, 2)
                                  end AS avg_iri
                                    ,case when AVG(left_iri) =0 or AVG(right_iri)=0
                                                    then STDDEV(right_iri)+ STDDEV(left_iri)
                                            ELSE STDDEV((right_iri+left_iri)/2) end AS variation_iri
                                FROM
                                    evaluationmanagement_planenessdata_ls a
                                left join main_parttab b on a.part_id=b.id
                                where a.part_id=%s and a.surveyPlan_id=%s
                                group by lineCode,b.id) x group by lineCode,id
                                        ''', [currentPart.id,currentPlan.surveyPlanCode])
                PlanenessSevaluation = cursor.fetchall()
                cursor.close()
                for item in PlanenessSevaluation:
                    planeness_result_part.objects.create(
                        surveyPlan=currentPlan,
                        part = currentPart,
                        lineCode = item[1],
                        avg_iri = item[2],
                        cv = item[3],
                        level = item[4]
                    )
                ret['message'] = '保存成功。'
                ret['status'] = True
        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)
    return render(request, 'evaluationManagement/planeness/planenessData_sureOper.html')

def planenessData_analy(request,surveyPlanCode,partId):
    currentPlan = surveyPlan.objects.get(surveyPlanCode=surveyPlanCode)
    currentPart = PartTab.objects.get(id=partId)

    # IRI评价结果
    iri_data = planeness_result_part.objects.filter(surveyPlan=currentPlan,part=currentPart)
    iri_json=[]
    for item in iri_data:
        iri_json.append({'partName':item.part.partName+'('+item.part.airCode+')','lineCode':item.lineCode,
                          'avg_iri': str(item.avg_iri), 'cv': str(item.cv),
                          'level': item.level})

    # iri统计图
    cursor = connection.cursor()
    cursor.execute('''
        SELECT @rowno:=@rowno+1 as rowno,r.* from(
        SELECT
            lineCode,GROUP_CONCAT(stakeNo ORDER BY stakeNo),GROUP_CONCAT(case when left_iri=0 and right_iri=0 then '-' when left_iri=0 or right_iri=0 then left_iri+right_iri else (left_iri+right_iri)/2 end ORDER BY stakeNo )
        FROM
            evaluationmanagement_planenessdata
        WHERE
            part_id = %s
        AND surveyPlan_id = %s
        GROUP BY lineCode) r
         ,(select (@rowno:=0) ) t
    ''', [currentPart.id,currentPlan.surveyPlanCode])
    iri_data_ora = cursor.fetchall()


    context={
        'currentPlan':currentPlan,
        'currentPart':currentPart,
        'iri_json':iri_json,
        'chart_data':iri_data_ora
    }
    return render(request, 'evaluationManagement/planeness/planenessData_analy.html',context)