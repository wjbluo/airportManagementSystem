from django.conf.urls import url,include
from .views import *
urlpatterns = [
    # 损坏调查模块

    # 计划
    url(r'^damage/surveyPlan/$', initsurveyPlan, name='initsurveyPlan'),
    url(r'^damage/surveyPlan/planMenu/$', planMenu, name='planMenu'),

    url(r'^damage/surveyPlan/addPlan/$', addPlan, name='addPlan'),
    url(r'^damage/surveyPlan/addPlan/selectObject/$', selectObject, name='selectObject'),
    url(r'^damage/surveyPlan/addPlan/setObject/$', setObject, name='setObject'),
    url(r'^damage/surveyPlan/addPlanSubmit/$', addPlanSubmit, name='addPlanSubmit'),
    url(r'^damage/surveyPlan/showPlan/(?P<surveyPlanCode>[\d]+)/$', showPlan, name='showPlan'),

    url(r'^downloadStaticFile/(?P<fileType>[\w]+)/$', downloadStaticFile, name='downloadStaticFile'),

    # 损坏记录余评价
    url(r'^damage/damageRecordsAndEvaluation/$', initDamageRecordsAndEvaluation, name='initDamageRecordsAndEvaluation'),
    url(r'^damage/damageRecordsAndEvaluation/damageMenu/(?P<Type>[123])/$', damageMenu, name='damageMenu'),
    # 损坏记录
    url(r'^damage/damageRecordsAndEvaluation/damageData/(?P<surveyPlanCode>[\d]{14})/(?P<areaId>[\d]+)/$', showDamageData, name='damageData'),
    url(r'^damage/damageRecordsAndEvaluation/damageData/sureData/$', sureData,name='sureData'),
    url(r'^damage/damageRecordsAndEvaluation/searchDamageData/(?P<surveyPlanCode>[\d]{14})/(?P<areaId>[\d]+)/$', searchDamageData, name='searchDamageData'),
    url(r'^damage/damageRecordsAndEvaluation/damageData/(?P<surveyPlanCode>[\d]{14})/(?P<areaId>[\d]+)/uploadDamageData/$', uploadDamageData, name='uploadDamageData'),
    url(r'^damage/damageRecordsAndEvaluation/damageData/(?P<surveyPlanCode>[\d]{14})/(?P<areaId>[\d]+)/uploadPic/$', uploadPic,
        name='uploadPic'),
    url(r'^damage/damageRecordsAndEvaluation/damageData/(?P<surveyPlanCode>[\d]{14})/(?P<areaId>[\d]+)/uploadPic/receivePic/$',
        receivePic,
        name='receivePic'),
    url(r'^damage/damageRecordsAndEvaluation/delDamageData/$',delDamageData,name='delDamageData'),
    url(r'^damage/damageRecordsAndEvaluation/damageData/(?P<surveyPlanCode>[\d]{14})/(?P<areaId>[\d]+)/lookAllPic/$',lookAllPic,name='lookAllPic'),
    #PCI计算
    url(r'^damage/damageRecordsAndEvaluation/pciCalData/(?P<surveyPlanCode>[\d]{14})/(?P<areaId>[\d]+)/$', pciCalData, name='pciCalData'),
    # 道面损坏统计
    url(r'^damage/damageStatistics/$',initdamageStatisticsFrame,name='damageStatisticsFrame'),
    url(r'^damage/damageStatistics/statMenu/(?P<Type>[123])/$',statMenu,name='statMenu'),
    url(r'^damage/damageStatistics/damageStat/(?P<surveyPlanCode>[\d]{14})/(?P<areaId>[\d]+)/$', damageStat, name='damageStat'),
    url(r'^damage/damageStatistics/damageStat/changeSelect/(?P<type>[\w]+)/$', changeSelect, name='changeSelect'),
    url(r'^damage/damageStatistics/damageStat/getPicData/$', getPicData, name='getPicData'),

    # 弯沉测试预评价
    url(r'^deflection/RecordsAndEvaluation/$', initDeflectionRecordsAndEvaluation, name='initDeflectionRecordsAndEvaluation'),
    url(r'^deflection/RecordsAndEvaluation/deflectionData/(?P<surveyPlanCode>[\d]{14})/(?P<areaId>[\d]+)/$', deflectionData, name='deflectionData'),
    url(r'^deflection/RecordsAndEvaluation/deflectionData/(?P<surveyPlanCode>[\d]{14})/(?P<areaId>[\d]+)/uploadDeflectData/$', uploadDeflectData, name='uploadDeflectData'),
    url(r'^deflection/RecordsAndEvaluation/searchDeflectData/(?P<surveyPlanCode>[\d]{14})/(?P<areaId>[\d]+)/$',
        searchDeflectData, name='searchDeflectData'),
    url(r'^deflection/RecordsAndEvaluation/deflectionData/sureDeflectData/$', sureDeflectData, name='sureDeflectData'),
    url(r'^deflection/RecordsAndEvaluation/deflectionData/editDeflectData/$', editDeflectData, name='editDeflectData'),
    url(r'^deflection/RecordsAndEvaluation/deflectionData/delDeflectData/$', delDeflectData, name='delDeflectData'),

    #接缝性能评价
    url(r'^deflection/RecordsAndEvaluation/deflectData_analy/(?P<surveyPlanCode>[\d]{14})/(?P<areaId>[\d]+)/$', deflectData_analy,
        name='deflectData_analy'),

    # 平整度测试预评价
    url(r'^planeness/RecordsAndEvaluation/$', initPlanenessRecordsAndEvaluation,name='initPlanenessRecordsAndEvaluation'),
    url(r'^planeness/RecordsAndEvaluation/planenessData/(?P<surveyPlanCode>[\d]{14})/(?P<partId>[\d]+)/$', showplanenessData,name='planenessData'),
    url(r'^planeness/RecordsAndEvaluation/planenessData/(?P<surveyPlanCode>[\d]{14})/(?P<partId>[\d]+)/uploadPlanenessData/$', uploadPlanenessData, name='uploadPlanenessData'),
    url(r'^planeness/RecordsAndEvaluation/searchPlanenessData/(?P<surveyPlanCode>[\d]{14})/(?P<partId>[\d]+)/$',
        searchPlanenessData, name='searchPlanenessData'),
    url(r'^planeness/RecordsAndEvaluation/planenessData/surePlanenessData/$', surePlanenessData, name='surePlanenessData'),
    url(r'^planeness/RecordsAndEvaluation/planenessData_analy/(?P<surveyPlanCode>[\d]{14})/(?P<partId>[\d]+)/$',
        planenessData_analy,
        name='planenessData_analy'),


]
