from django.db import models
from main.models import AreaTab,PartTab
# Create your models here.
# 项目计划表
class surveyPlan(models.Model):
    surveyPlanCode = models.CharField(max_length=20, verbose_name='项目编号',primary_key=True)
    year = models.CharField(max_length=4, verbose_name='年度')
    startTime=models.CharField(max_length=10, verbose_name='开始时间')
    endTime = models.CharField(max_length=10, verbose_name='结束时间')
    evaluationUnit = models.CharField(max_length=50, verbose_name='评估单位')
    remark =  models.CharField(max_length=500, verbose_name='备注')


    def __str__(self):
        return self.surveyPlanCode

    class Meta:
        verbose_name='项目计划表'
        verbose_name_plural = verbose_name
        ordering = ['surveyPlanCode']

# 项目内容条目
class assessmentItems(models.Model):
    surveyPlan = models.ForeignKey(surveyPlan, db_constraint=True, verbose_name='项目编号')
    area = models.ForeignKey(AreaTab, verbose_name='区域')
    assessmentItem = models.CharField(max_length=5, verbose_name='评估内容')
    assessmentItem1_sureFlag = models.CharField(max_length=1, verbose_name='评估内容1是否确认标志位',default='0')
    Date_1 =  models.CharField(max_length=10, verbose_name='评估1日期')
    oper_1 = models.CharField(max_length=10, verbose_name='评估1记录人')
    assessmentItem2_sureFlag = models.CharField(max_length=1, verbose_name='评估内容2是否确认标志位',default='0')
    Date_2 =  models.CharField(max_length=10, verbose_name='评估2日期')
    oper_2 = models.CharField(max_length=10, verbose_name='评估2记录人')
    suface_Tem_2 = models.CharField(max_length=10, verbose_name='评估2地表温度')
    bearingplate_radius_2 = models.CharField(max_length=10, verbose_name='评估2承载板半径')
    distance_2 = models.CharField(max_length=10, verbose_name='评估2测点间距')
    assessmentItem3_sureFlag = models.CharField(max_length=1, verbose_name='评估内容3是否确认标志位',default='0')
    Date_3 =  models.CharField(max_length=10, verbose_name='评估3日期')
    oper_3 = models.CharField(max_length=10, verbose_name='评估3记录人')
    measuringLine_length_3 = models.CharField(max_length=10, verbose_name='评估内容3测线长度')
    samplingDistance_3 = models.CharField(max_length=10, verbose_name='评估内容3采样间距')
    testDesc_3 = models.CharField(max_length=200, verbose_name='评估内容3测试描述')

    def __str__(self):
        return self.surveyPlan.surveyPlanCode

    class Meta:
        verbose_name='评估条目表'
        verbose_name_plural = verbose_name
        ordering = ['id']


# 损坏数据__临时
class damageData_ls(models.Model):
    surveyPlan = models.ForeignKey(surveyPlan, verbose_name='项目编号')
    area = models.ForeignKey(AreaTab, verbose_name='所属区域')
    cell = models.CharField(max_length=20, verbose_name='单元名称')
    damageType = models.IntegerField(verbose_name='病害类型',default=0)
    damageDegree = models.CharField(max_length=10, verbose_name='病害程度')
    damageNumber = models.DecimalField(verbose_name='病害数量',default=0,max_digits=5, decimal_places=2)
    damageUnit =  models.CharField(max_length=10, verbose_name='病害单位')
    palteRow = models.CharField(max_length=10,verbose_name='板块行编号')
    palteCol = models.CharField(max_length=10,verbose_name='板块列编号')
    palteX = models.CharField(max_length=10,verbose_name='X坐标')
    palteY = models.CharField(max_length=10,verbose_name='Y坐标')
    diseasephoto = models.CharField(max_length=100,verbose_name='病害图片',default='',blank=True, null=True)


    def __str__(self):
        return self.surveyPlan.surveyPlanCode

    class Meta:
        verbose_name='损坏数据临时表'
        verbose_name_plural = verbose_name
        ordering = ['id']

    # 弯沉数据__临时
class deflectData_ls(models.Model):
    surveyPlan = models.ForeignKey(surveyPlan, verbose_name='项目编号')
    area = models.ForeignKey(AreaTab, verbose_name='所属区域')
    plateCode = models.CharField(max_length=20, verbose_name='板编号')
    loadPosition = models.CharField(max_length=20,verbose_name='荷位')
    D1 = models.CharField(max_length=20, verbose_name='D1')
    D2 = models.CharField(max_length=20, verbose_name='D2')
    D3 = models.CharField(max_length=20, verbose_name='D3')
    D4 = models.CharField(max_length=20, verbose_name='D4')
    D5 = models.CharField(max_length=20, verbose_name='D5')
    D6 = models.CharField(max_length=20, verbose_name='D6')
    D7 = models.CharField(max_length=20, verbose_name='D7')
    D8 = models.CharField(max_length=20, verbose_name='D8')
    D9 = models.CharField(max_length=20, verbose_name='D9')
    load = models.CharField(max_length=20, verbose_name='load')

    def __str__(self):
        return self.surveyPlan.surveyPlanCode+self.plateCode

    class Meta:
        verbose_name = '损坏数据临时表'
        verbose_name_plural = verbose_name

# 平整度数据__临时
class planenessData_ls(models.Model):
    surveyPlan = models.ForeignKey(surveyPlan, verbose_name='项目编号')
    part = models.ForeignKey(PartTab, verbose_name='所属部位')
    lineCode = models.CharField(max_length=20, verbose_name='测线名称')
    stakeNo = models.DecimalField(verbose_name='桩号',default=0, max_digits=7, decimal_places=2)
    left_iri = models.DecimalField(verbose_name='左IRI',default=0,max_digits=5, decimal_places=2)
    left_variance = models.DecimalField(default=0,max_digits=5, decimal_places=2, verbose_name='左方差')
    right_iri = models.DecimalField(verbose_name='右IRI',default=0,max_digits=5, decimal_places=2)
    right_variance = models.DecimalField(default=0,max_digits=5, decimal_places=2, verbose_name='右方差')

    def __str__(self):
        return self.surveyPlan.surveyPlanCode + self.lineCode

    class Meta:
        verbose_name = '平整度数据__临时'
        verbose_name_plural = verbose_name

# 平整度数据__正式
class planenessData(models.Model):
    surveyPlan = models.ForeignKey(surveyPlan, verbose_name='项目编号')
    part = models.ForeignKey(PartTab, verbose_name='所属部位')
    lineCode = models.CharField(max_length=20, verbose_name='测线名称')
    stakeNo = models.DecimalField(verbose_name='桩号',default=0, max_digits=7, decimal_places=2)
    left_iri = models.DecimalField(verbose_name='左IRI', default=0, max_digits=5, decimal_places=2)
    left_variance = models.DecimalField(default=0, max_digits=5, decimal_places=2, verbose_name='左方差')
    right_iri = models.DecimalField(verbose_name='右IRI', default=0, max_digits=5, decimal_places=2)
    right_variance = models.DecimalField(default=0, max_digits=5, decimal_places=2, verbose_name='右方差')
    iri_avg =  models.DecimalField(default=0, max_digits=5, decimal_places=2, verbose_name='平均iri')

    def __str__(self):
        return self.surveyPlan.surveyPlanCode + self.lineCode

    class Meta:
        verbose_name = '平整度数据__临时'
        verbose_name_plural = verbose_name

    # 弯沉数据__正式

class deflectData(models.Model):
    surveyPlan = models.ForeignKey(surveyPlan, verbose_name='项目编号')
    area = models.ForeignKey(AreaTab, verbose_name='所属区域')
    plateCode = models.CharField(max_length=20, verbose_name='板编号')
    loadPosition = models.CharField(max_length=20, verbose_name='荷位')
    D1 = models.CharField(max_length=20, verbose_name='D1')
    D2 = models.CharField(max_length=20, verbose_name='D2')
    D3 = models.CharField(max_length=20, verbose_name='D3')
    D4 = models.CharField(max_length=20, verbose_name='D4')
    D5 = models.CharField(max_length=20, verbose_name='D5')
    D6 = models.CharField(max_length=20, verbose_name='D6')
    D7 = models.CharField(max_length=20, verbose_name='D7')
    D8 = models.CharField(max_length=20, verbose_name='D8')
    D9 = models.CharField(max_length=20, verbose_name='D9')
    load = models.CharField(max_length=20, verbose_name='load')

    def __str__(self):
        return self.surveyPlan.surveyPlanCode + self.plateCode

    class Meta:
        verbose_name = '弯沉数据'
        verbose_name_plural = verbose_name

# 损坏数据__正式
class damageData(models.Model):
    surveyPlan = models.ForeignKey(surveyPlan, verbose_name='项目编号')
    area = models.ForeignKey(AreaTab, verbose_name='所属区域')
    cell = models.CharField(max_length=20, verbose_name='单元名称')
    damageType = models.IntegerField(verbose_name='病害类型',default=0)
    damageDegree = models.CharField(max_length=10, verbose_name='病害程度')
    damageNumber = models.DecimalField(verbose_name='病害数量',default=0,max_digits=5, decimal_places=2)
    damageUnit =  models.CharField(max_length=10, verbose_name='病害单位')
    palteRow = models.CharField(max_length=10,verbose_name='板块行编号')
    palteCol = models.CharField(max_length=10,verbose_name='板块列编号')
    palteX = models.CharField(max_length=10,verbose_name='X坐标')
    palteY = models.CharField(max_length=10,verbose_name='Y坐标')
    diseasephoto = models.CharField(max_length=100,verbose_name='病害图片',default='',blank=True, null=True)


    def __str__(self):
        return self.surveyPlan.surveyPlanCode

    class Meta:
        verbose_name='损坏数据表'
        verbose_name_plural = verbose_name

# 区域PCI结果存放
class PCI_result_area(models.Model):
    surveyPlan = models.ForeignKey(surveyPlan, verbose_name='项目编号')
    area = models.ForeignKey(AreaTab, verbose_name='所属区域')
    areaPCI = models.DecimalField(verbose_name='区域PCI',default=0,max_digits=5, decimal_places=2)
    areaSCI = models.DecimalField(verbose_name='区域SCI',default=0,max_digits=5, decimal_places=2)
    level = models.CharField(max_length=10,verbose_name='评价等级')
    PCI_coefficient = models.DecimalField(verbose_name='PCI变异系数',default=0,max_digits=5, decimal_places=2)

    def __str__(self):
        return self.surveyPlan.surveyPlanCode+self.area.areaCode+'PCI'

    class Meta:
        verbose_name='区域PCI结果存放'
        verbose_name_plural = verbose_name
        ordering = ['id']

# 区域接缝性能评价 数据存放
class join_result_area(models.Model):
    surveyPlan = models.ForeignKey(surveyPlan, verbose_name='项目编号')
    area = models.ForeignKey(AreaTab, verbose_name='所属区域')
    avg = models.DecimalField(verbose_name='脱空均值%', default=0, max_digits=5, decimal_places=2)
    level_good = models.DecimalField(verbose_name='好（>80%）', default=0, max_digits=5, decimal_places=2)
    level_mid = models.DecimalField(verbose_name='中（56%-80%）', default=0, max_digits=5, decimal_places=2)
    level_ci = models.DecimalField(verbose_name='次（31%-56%）', default=0, max_digits=5, decimal_places=2)
    level_cha = models.DecimalField(verbose_name='差（<56%）', default=0, max_digits=5, decimal_places=2)

    def __str__(self):
        return self.surveyPlan.surveyPlanCode + self.area.areaCode + 'join'

    class Meta:
        verbose_name = '区域接缝性能评价 数据存放'
        verbose_name_plural = verbose_name
# 平整度数据存放
class planeness_result_part(models.Model):
    surveyPlan = models.ForeignKey(surveyPlan, verbose_name='项目编号')
    part = models.ForeignKey(PartTab, verbose_name='所属部位')
    lineCode = models.CharField(max_length=20, verbose_name='测线名称')
    avg_iri = models.DecimalField(verbose_name='IRI均值', default=0, max_digits=5, decimal_places=2)
    cv = models.DecimalField(verbose_name='变异系数', default=0, max_digits=5, decimal_places=2)
    level = models.CharField(max_length=20, verbose_name='评价等级')


    def __str__(self):
        return self.surveyPlan.surveyPlanCode + self.part.partCode + 'planeness'


    class Meta:
        verbose_name = '平整度评价 数据存放'
        verbose_name_plural = verbose_name


# 脱空性能评价 数据存放
class void_result_area(models.Model):
    surveyPlan = models.ForeignKey(surveyPlan, verbose_name='项目编号')
    area = models.ForeignKey(AreaTab, verbose_name='所属区域')
    bian_zhong_avg = models.DecimalField(verbose_name='板边/板中均值', default=0, max_digits=5, decimal_places=2)
    bian_zhong_max = models.DecimalField(verbose_name='板边/板中最大值', default=0, max_digits=5, decimal_places=2)
    bian_zhong_min = models.DecimalField(verbose_name='板边/板中最小值', default=0, max_digits=5, decimal_places=2)
    bian_radio_2_3 = models.DecimalField(verbose_name='板边脱空比例（2,3）%', default=0, max_digits=5, decimal_places=2)
    bian_radio_3_6 = models.DecimalField(verbose_name='板边脱空比例（3.5,6）%', default=0, max_digits=5, decimal_places=2)
    jiao_zhong_avg = models.DecimalField(verbose_name='板角/板中均值', default=0, max_digits=5, decimal_places=2)
    jiao_zhong_max = models.DecimalField(verbose_name='板角/板中最大值', default=0, max_digits=5, decimal_places=2)
    jiao_zhong_min = models.DecimalField(verbose_name='板角/板中最小值', default=0, max_digits=5, decimal_places=2)
    jiao_radio_2_3 = models.DecimalField(verbose_name='板角脱空比例（2,3）%', default=0, max_digits=5, decimal_places=2)
    jiao_radio_3_6 = models.DecimalField(verbose_name='板角脱空比例（3.5,6）%', default=0, max_digits=5, decimal_places=2)
    radio_2_3 = models.DecimalField(verbose_name='总脱空比例（2,3）%', default=0, max_digits=5, decimal_places=2)
    radio_3_6 = models.DecimalField(verbose_name='总脱空比例（3.5,6）%', default=0, max_digits=5, decimal_places=2)

    def __str__(self):
        return self.surveyPlan.surveyPlanCode + self.area.areaCode + 'void'

    class Meta:
        verbose_name = '脱空性能评价 数据存放'
        verbose_name_plural = verbose_name

# 参数表
class parameterTab(models.Model):
    parameterType = models.CharField(max_length=10,verbose_name='参数类型')
    parameterCode = models.CharField(max_length=10,verbose_name='参数编号')
    parameterName = models.CharField(max_length=100, verbose_name='参数名称')
    extra = models.CharField(max_length=100, verbose_name='扩展字段_备用')

    def __str__(self):
        return self.parameterName

    class Meta:
        verbose_name='参数表'
        verbose_name_plural = verbose_name