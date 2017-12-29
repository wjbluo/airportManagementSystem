from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# ###########权限相关表
# 角色表     类似于部门  在角色中的人均拥有固定权限。
class roleTab(models.Model):
    roleName = models.CharField(max_length=50, verbose_name='角色名称')
    roleDis = models.CharField(max_length=500, verbose_name='角色描述')


    def __str__(self):
        return self.roleName

    class Meta:
        verbose_name='角色表'
        verbose_name_plural = verbose_name
        ordering = ['id']

# 权限表
class permissionTab(models.Model):
    menuId = models.CharField(max_length=10, verbose_name='菜单编号')
    menuTitle = models.CharField(max_length=50, verbose_name='菜单名称')
    icon = models.CharField(max_length=10, verbose_name='菜单icon')
    url = models.CharField(max_length=100, verbose_name='菜单url')
    isCurrent = models.CharField(max_length=1, verbose_name='是否默认打开')

    parentmenuId = models.CharField(max_length=10, verbose_name='父级菜单编号')
    level = models.CharField(max_length=10, verbose_name='顺序级别')

    def __str__(self):
        return self.menuTitle

    class Meta:
        verbose_name = '权限菜单表'
        verbose_name_plural = verbose_name
        ordering = ['id']

# 员工角色表
class user_roleTab(models.Model):
    user = models.ForeignKey(User, db_constraint=True, verbose_name='用户')
    role = models.ForeignKey(roleTab, db_constraint=True, verbose_name='角色')


    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name='员工角色表'
        verbose_name_plural = verbose_name
        ordering = ['id']

# 角色权限表
class role_permissionTab(models.Model):
    role = models.ForeignKey(roleTab, db_constraint=True, verbose_name='角色')
    persission = models.ForeignKey(permissionTab, db_constraint=True, verbose_name='角色')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name='角色权限表'
        verbose_name_plural = verbose_name
        ordering = ['id']

# ########### 基本数据表
# 机场基本信息表
class airport_baseData(models.Model):
    airportName = models.CharField(max_length=100, verbose_name='机场名称')
    airportCode = models.CharField(max_length=10, verbose_name='机场编码')
    manageInstitution = models.CharField(max_length=100, verbose_name='管理机构')
    airportLevel = models.CharField(max_length=10, verbose_name='机场等级')
    runwayNum = models.IntegerField(verbose_name='跑道数量')
    smoothRoadNum = models.IntegerField(verbose_name='平滑道数量')
    roadSurfaceArea = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='道面面积')
    soilSurfaceArea = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='土面面积')
    seatOfPlaneNum = models.IntegerField(verbose_name='机位数量')
    shippingTime = models.CharField(max_length=50, verbose_name='通航时间')
    recordingTime = models.CharField(max_length=25, verbose_name='记录时间')
    updateTime = models.CharField(max_length=50, verbose_name='更新时间')

    def __str__(self):
        return self.airportName

    class Meta:
        verbose_name='机场基本信息表'
        verbose_name_plural = verbose_name
        ordering = ['id']

# 跑道基本信息表
class runway_baseData(models.Model):
    runwayName = models.CharField(max_length=100, verbose_name='跑道名称')
    runwayCode = models.CharField(max_length=10, verbose_name='跑道标志码')
    airport = models.ForeignKey(airport_baseData, db_constraint=True, verbose_name='所属机场')
    sizeOfRunway = models.CharField(max_length=10, verbose_name='跑道尺寸')
    sizeOfLiftingBelt = models.CharField(max_length=10, verbose_name='升降带尺寸')
    sizeOfBlastPad = models.CharField(max_length=10, verbose_name='防吹坪尺寸')
    widthOfShoulder = models.CharField(max_length=10, verbose_name='道肩宽度')
    sizeOfSafetyZone = models.CharField(max_length=10, verbose_name='端安全区尺寸')
    operationCategory1 = models.CharField(max_length=10, verbose_name='运行类别1')
    operationCategory2 = models.CharField(max_length=10, verbose_name='运行类别2')
    takeoffDistance = models.CharField(max_length=10, verbose_name='可用起飞距离')
    takeoffRunDistance = models.CharField(max_length=10, verbose_name='可用起飞滑跑距离')
    runwayFrictionCoefficient = models.CharField(max_length=10, verbose_name='摩擦系数')
    landingDistance = models.CharField(max_length=10, verbose_name='可用着陆距离')
    accelerateStopDistance = models.CharField(max_length=10, verbose_name='可用加速停止距离')
    crossSlope = models.CharField(max_length=10, verbose_name='横坡')
    effectiveLongitudinalSlope = models.CharField(max_length=10, verbose_name='有效纵坡')
    bulletinPCN = models.CharField(max_length=10, verbose_name='通报PCN')
    shippingTime = models.CharField(max_length=50, verbose_name='通航时间')
    recordingTime = models.CharField(max_length=25, verbose_name='记录时间')
    updateTime = models.CharField(max_length=50, verbose_name='更新时间')

    def __str__(self):
        return self.runwayName

    class Meta:
        verbose_name = '跑道基本信息表'
        verbose_name_plural = verbose_name
        ordering = ['id']

# 部位表
class PartTab(models.Model):
    airport = models.ForeignKey(airport_baseData, db_constraint=True, verbose_name='所属机场')
    partCode = models.CharField(max_length=10, verbose_name='部位编码')
    partName = models.CharField(max_length=50, verbose_name='部位名称')
    partDis =  models.CharField(max_length=500, verbose_name='功能描述',default='')
    airCode = models.CharField(max_length=10, verbose_name='机场编号',default='')
    containsAreaNum = models.CharField(max_length=10, verbose_name='包含区域',default='')
    containsStructureNum = models.CharField(max_length=10, verbose_name='包含结构',default='')
    partLevel = models.CharField(max_length=10, verbose_name='重要等级',default='')
    recordingTime = models.CharField(max_length=25, verbose_name='记录时间',default='')
    updateTime = models.CharField(max_length=50, verbose_name='更新时间',default='')

    def __str__(self):
        return self.partName

    class Meta:
        verbose_name = '跑道部位信息表'
        verbose_name_plural = verbose_name
        ordering = ['id']

# 区域表
class AreaTab(models.Model):
    part = models.ForeignKey(PartTab, db_constraint=True, verbose_name='所属部位')
    areaCode = models.CharField(max_length=10, verbose_name='区域编码')
    areaDis = models.CharField(max_length=500, verbose_name='区域位置')
    areaStruct = models.CharField(max_length=50, verbose_name='结构类型')
    structCode = models.CharField(max_length=20, verbose_name='结构组合',default='')
    recordingTime = models.CharField(max_length=25, verbose_name='记录时间', default='')
    updateTime = models.CharField(max_length=50, verbose_name='更新时间')

    def __str__(self):
        return self.areaCode

    def getDisplayAreaCode(self):
        return self.part.partCode+self.areaCode

    class Meta:
        verbose_name = '跑道部位信息表'
        verbose_name_plural = verbose_name
        ordering = ['id']

# 单元表
class cellTab(models.Model):
    area = models.ForeignKey(AreaTab, db_constraint=True, verbose_name='所属区域')
    cellCode = models.CharField(max_length=10, verbose_name='单元编码')
    recordingTime = models.CharField(max_length=25, verbose_name='记录日期')
    updateTime = models.CharField(max_length=50, verbose_name='更新时间',default='')

    def __str__(self):
        return self.cellCode

    def getDisplayCellCode(self):
        return self.area.part.partCode+self.area.areaCode+'-'+self.cellCode

    class Meta:
        verbose_name = '单元表'
        verbose_name_plural = verbose_name
        ordering = ['id']

# 板块表
class plateTab(models.Model):
    cell = models.ForeignKey(cellTab, db_constraint=True, verbose_name='所属单元')
    rowNo = models.CharField(max_length=10, verbose_name='行编号')
    colNo = models.CharField(max_length=10, verbose_name='列编号')
    platelength = models.CharField(max_length=10, verbose_name='长度')
    width = models.CharField(max_length=10, verbose_name='宽度')
    area = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='面积')
    shape = models.CharField(max_length=50, verbose_name='形状')
    recordingTime = models.CharField(max_length=25, verbose_name='记录日期')
    updateTime = models.CharField(max_length=50, verbose_name='更新时间')

    def __str__(self):
        return self.cell.cellCode+'的板块'

    class Meta:
        verbose_name = '板块表'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def get_total_area(self):
        return sum(float(item.area) for item in self)

class structureComposition(models.Model):
    structureClass = models.CharField(max_length=10, verbose_name='类别')
    structureCode = models.CharField(max_length=10, verbose_name='结构编号')

    def __str__(self):
        return self.structureClass

    class Meta:
        verbose_name = '结构组合表'
        verbose_name_plural = verbose_name
        ordering = ['id']

class structure(models.Model):
    structureCode = models.CharField(max_length=10, verbose_name='结构编号')
    layerCode = models.CharField(max_length=10, verbose_name='层次编号')
    materialName = models.CharField(max_length=50, verbose_name='材料名称')
    thickness = models.CharField(max_length=10, verbose_name='厚度')
    elasticModulus = models.CharField(max_length=10, verbose_name='弹性模量')
    CBR = models.CharField(max_length=10, verbose_name='CBR')
    poissonRatio = models.CharField(max_length=10, verbose_name='泊松比')
    recordingTime = models.CharField(max_length=25, verbose_name='记录日期')
    updateTime = models.CharField(max_length=50, verbose_name='更新时间')

    def __str__(self):
        return self.structureCode

    class Meta:
        verbose_name = '结构表'
        verbose_name_plural = verbose_name
        ordering = ['id']