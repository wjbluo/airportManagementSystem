from django.db import models
from main.models import runway_baseData,cellTab
from evaluationManagement.models import parameterTab
from django.contrib.auth.models import User
# Create your models here.
class runwaysPatroData(models.Model):
    taskNo = models.CharField(max_length=20, verbose_name='任务编号',primary_key=True)
    taskType = models.CharField(max_length=2, verbose_name='任务类型',default='ph')
    weather = models.CharField(max_length=100, verbose_name='天气')
    patroDate = models.CharField(max_length=8, verbose_name='巡视日期')
    runways_id = models.CharField(max_length=10, verbose_name='跑道id',default='')
    patroCount = models.CharField(max_length=50, verbose_name='巡视类型')
    patrolReason = models.CharField(max_length=50, verbose_name='巡视原因',default='')
    patroMainCar =  models.CharField(max_length=10, verbose_name='巡视主车')
    mainCarPerson =  models.CharField(max_length=100, verbose_name='主车人员')
    mainCarDirection = models.CharField(max_length=10, verbose_name='主车方向')
    mainCarTrail = models.CharField(max_length=100, verbose_name='主车巡视轨迹')
    sideCar =  models.CharField(max_length=10, verbose_name='巡视副车')
    sideCarPerson = models.CharField(max_length=100, verbose_name='副车人员')
    sideCarDirection = models.CharField(max_length=10, verbose_name='副车方向')
    sideCarTrail = models.CharField(max_length=100, verbose_name='副车巡视轨迹')

    carryGoods = models.CharField(max_length=20, verbose_name='携带物品')

    notifiedTowerTime = models.CharField(max_length=50, verbose_name='通知塔台时间')
    notifiedFlyingTime = models.CharField(max_length=50, verbose_name='通知飞管时间')

    entryTime = models.CharField(max_length=10, verbose_name='进入巡视时间')
    exitWaitingPosition = models.CharField(max_length=10, verbose_name='退出等待位置')
    exitWaitingTime = models.CharField(max_length=50, verbose_name='退出等待时间')
    Re_entryTime = models.CharField(max_length=10, verbose_name='再次进入巡视时间')

    exitNotifiedTowerTime = models.CharField(max_length=50, verbose_name='退出通知塔台时间')
    exitNotifiedFlyingTime = models.CharField(max_length=50, verbose_name='退出通知飞管时间')
    exitTime = models.CharField(max_length=10, verbose_name='结束巡视时间')

    noPatroReason = models.CharField(max_length=200, verbose_name='未巡视原因')
    radioDis = models.CharField(max_length=500, verbose_name='视频地址',default='')
    flag = models.CharField(max_length=1, verbose_name='标志位')


    def __str__(self):
        return self.taskNo

    def showPatrolCount(self):
        para = parameterTab.objects.get(parameterType='patrolType',parameterCode=self.patroCount)
        patrolName =para.parameterName
        if self.patroCount == '05':
            patrolName+='<'+self.patrolReason+'>'
        return para.parameterName

    def showMainPersonal(self):
        mainCarPerson_list = self.mainCarPerson.split(';')
        mainCarPerson_str = ''
        for item in mainCarPerson_list:
            if item != '':
                this_User = User.objects.get(id=int(item))
                if this_User:
                    mainCarPerson_str += this_User.first_name + this_User.last_name + ' ; '
        return mainCarPerson_str

    def showSidePersonal(self):
        sideCarPerson_list = self.sideCarPerson.split(';')
        sideCarPerson_str = ''
        for item in sideCarPerson_list:
            if item != '':
                this_User = User.objects.get(id=int(item))
                if this_User:
                    sideCarPerson_str += this_User.first_name + this_User.last_name + ' ; '
        return sideCarPerson_str

    def showTools(self):
        tools_list = self.carryGoods.split(';')
        tools_str = ''
        for item in tools_list:
            if item != '':
                tool = parameterTab.objects.get(parameterType='patrolItem',parameterCode=item)
                if tool:
                    tools_str += tool.parameterName+ ' , '
        return tools_str

    class Meta:
        verbose_name='跑滑巡视记录'
        verbose_name_plural = verbose_name

class runwaysDamageData(models.Model):
    Patro = models.ForeignKey(runwaysPatroData, db_constraint=True, verbose_name='巡视记录')
    damageNo = models.AutoField(auto_created=True, verbose_name='异常', primary_key=True)
    runwayType = models.CharField(max_length=2, verbose_name='道面类型')
    damageType = models.CharField(max_length=2, verbose_name='损害类型')
    partitionCode = models.CharField(max_length=10, verbose_name='分区编号')
    Row = models.CharField(max_length=10,verbose_name='板块行编号')
    Col = models.CharField(max_length=10,verbose_name='板块列编号')
    X = models.CharField(max_length=10,verbose_name='X坐标')
    Y = models.CharField(max_length=10,verbose_name='Y坐标')
    location = models.CharField(max_length=50,verbose_name='位置区域')
    damageLength = models.CharField(verbose_name='损害长度',max_length=10,)
    damageWidth = models.CharField(verbose_name='损害宽度',max_length=10,)
    damageArea = models.CharField(verbose_name='损害面积',max_length=10,)

    desc = models.CharField(max_length=200,verbose_name='备注说明')
    damagePic = models.CharField(max_length=500,verbose_name='损害图片地址',default='')

    def __str__(self):
        return self.damageNo

    def showRunwaysType(self):
        para = parameterTab.objects.get(parameterType='patrolDam',parameterCode=self.runwayType)
        return para.parameterName
    def showDamageType(self):
        para = parameterTab.objects.get(parameterType='damageType',parameterCode=self.damageType)
        return para.parameterName
    def showDeaultAmount(self):
        if self.damageLength!='':
            return self.damageLength+'cm'
        if self.damageWidth!='':
            return self.damageWidth+'cm'
        if self.damageArea!='':
            return self.damageArea+'&sup2;'
    def showLength(self):
        if self.damageLength!='':
            return self.damageLength+'cm'
        else:
            return ''
    def showWidth(self):
        if self.damageWidth!='':
            return self.damageWidth+'cm'
        else:
            return ''
    def showArea(self):
        if self.damageArea!='':
            return self.damageArea+'m&sup2;'
        else:
            return ''

    def damagePicDir(self):
        dir_list = self.damagePic.split(';')
        dir = []
        for item in dir_list:
            if item!='':
                dir.append(item)
        return dir

    class Meta:
        verbose_name='跑滑巡视异常记录'
        verbose_name_plural = verbose_name


class runwaysDamageData_ls(models.Model):
    runwayType = models.CharField(max_length=2, verbose_name='道面类型')
    damageType = models.CharField(max_length=2, verbose_name='损害类型')
    partitionCode = models.CharField(max_length=10, verbose_name='分区编号')
    Row = models.CharField(max_length=10,verbose_name='板块行编号')
    Col = models.CharField(max_length=10,verbose_name='板块列编号')
    X = models.CharField(max_length=10,verbose_name='X坐标')
    Y = models.CharField(max_length=10,verbose_name='Y坐标')
    location = models.CharField(max_length=50,verbose_name='位置区域')
    damageLength = models.CharField(verbose_name='损害长度',max_length=10,)
    damageWidth = models.CharField(verbose_name='损害宽度',max_length=10,)
    damageArea = models.CharField(verbose_name='损害面积',max_length=10,)

    desc = models.CharField(max_length=200,verbose_name='备注说明')
    damagePic = models.CharField(max_length=500,verbose_name='损害图片地址',default='')

    def __str__(self):
        return self.damageNo

    class Meta:
        verbose_name='跑滑巡视异常记临时存放'
        verbose_name_plural = verbose_name