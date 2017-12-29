from django.db import models
from main.models import runway_baseData,cellTab
# Create your models here.
class runwaysPatroData(models.Model):
    taskNo = models.CharField(max_length=20, verbose_name='任务编号',primary_key=True)
    weather = models.CharField(max_length=100, verbose_name='天气')
    patroDate = models.CharField(max_length=4, verbose_name='巡视日期')
    runways = models.ForeignKey(runway_baseData, db_constraint=True, verbose_name='巡视跑道')
    patroCount = models.CharField(max_length=10, verbose_name='巡视类型')

    patroMainCar =  models.CharField(max_length=10, verbose_name='巡视主车')
    mainCarPerson =  models.CharField(max_length=100, verbose_name='主车人员')
    mainCarDirection = models.CharField(max_length=10, verbose_name='主车方向')
    mainCarTrail = models.CharField(max_length=100, verbose_name='主车巡视轨迹')
    sideCar =  models.CharField(max_length=10, verbose_name='巡视副车')
    sideCarPerson = models.CharField(max_length=100, verbose_name='副车人员')
    sideCarDirection = models.CharField(max_length=10, verbose_name='副车方向')
    sideCarTrail = models.CharField(max_length=100, verbose_name='副车巡视轨迹')

    carryGoods = models.CharField(max_length=10, verbose_name='携带物品')

    notifiedTowerTime = models.CharField(max_length=50, verbose_name='通知塔台时间')
    notifiedFlyingTime = models.CharField(max_length=50, verbose_name='通知飞管时间')

    entryTime = models.CharField(max_length=10, verbose_name='进入巡视时间')
    exitWaitingTime = models.CharField(max_length=50, verbose_name='退出等待时间')
    exitWaitingPosition = models.CharField(max_length=10, verbose_name='退出等待位置')
    exitWaitingTime = models.CharField(max_length=50, verbose_name='退出等待时间')
    Re_entryTime = models.CharField(max_length=10, verbose_name='再次进入巡视时间')

    exitNotifiedTowerTime = models.CharField(max_length=50, verbose_name='退出通知塔台时间')
    exitNotifiedFlyingTime = models.CharField(max_length=50, verbose_name='退出通知飞管时间')
    exitTime = models.CharField(max_length=10, verbose_name='结束巡视时间')

    noPatroReason = models.CharField(max_length=200, verbose_name='未巡视原因')
    flag = models.CharField(max_length=1, verbose_name='标志位')


    def __str__(self):
        return self.taskNo

    class Meta:
        verbose_name='跑滑巡视记录'
        verbose_name_plural = verbose_name

class runwaysDamageData(models.Model):
    Patro = models.ForeignKey(runwaysPatroData, db_constraint=True, verbose_name='巡视记录')
    damageNo = models.CharField(max_length=20, verbose_name='异常', primary_key=True)
    runwayType = models.CharField(max_length=1, verbose_name='道面类型')
    damageType = models.CharField(max_length=2, verbose_name='损害类型')
    partitionCode = models.CharField(max_length=10, verbose_name='分区编号')
    Row = models.CharField(max_length=10,verbose_name='板块行编号')
    Col = models.CharField(max_length=10,verbose_name='板块列编号')
    X = models.CharField(max_length=10,verbose_name='X坐标')
    Y = models.CharField(max_length=10,verbose_name='Y坐标')
    location = models.CharField(max_length=50,verbose_name='位置区域')
    damageLength = models.DecimalField(verbose_name='损害长度',default=0,max_digits=5, decimal_places=0)
    damageWidth = models.DecimalField(verbose_name='损害宽度', default=0, max_digits=5, decimal_places=0)
    damageArea = models.DecimalField(verbose_name='损害面积', default=0, max_digits=5, decimal_places=2)

    desc = models.CharField(max_length=200,verbose_name='备注说明')
    damagePic = models.CharField(max_length=500,verbose_name='损害图片地址',default='')

    def __str__(self):
        return self.damageNo

    class Meta:
        verbose_name='跑滑巡视异常记录'
        verbose_name_plural = verbose_name