from django.conf.urls import url,include
from .views import *
urlpatterns = [
    # 跑滑巡视模块
    url(r'^showPatrolRecord/$', showPatrolRecord, name='showPatrolRecord'),
    url(r'^showPatrolRecord/searchPatrolData/$', searchPatrolData, name='searchPatrolData'),
    url(r'^showPatrolRecord/printStandBook/(?P<taskNo>[\w]+)/$', printStandBook, name='printStandBook'),
    url(r'^showPatrolRecord/printStandBook/(?P<taskNo>[\w]+)/standBook/$', standBook, name='standBook'),

    url(r'^showPatrolRecord/printStandBook/savaAspdf_xsBook/(?P<taskNo>[\w]+)/(?P<posi>[\w]+)/$', savaAspdf_xsBook, name='savaAspdf_xsBook'),

    url(r'^showPatrolRecord/addPatrolRecord/$', addPatrolRecord, name='addPatrolRecord'),
    url(r'^showPatrolRecord/addPatrolRecord/addDamageRecord/$', addDamageRecord, name='addDamageRecord'),
    url(r'^showPatrolRecord/addPatrolRecord/receiveRadio/$', receiveRadio, name='receiveRadio'),
    url(r'^showPatrolRecord/addPatrolRecord/addDamageRecord/receiveDamagePic/$', receiveDamagePic, name='receiveDamagePic'),

    url(r'^showPatrolRecord/patrolRecordSubmit/$', patrolRecordSubmit, name='patrolRecordSubmit'),
    url(r'^showPatrolRecord/patrolDamageSubmit/$', patrolDamageSubmit, name='patrolDamageSubmit'),
    url(r'^showPatrolRecord/searchPatrolDamage/$', searchPatrolDamage, name='searchPatrolDamage'),

    url(r'^showPatrolRecord/(?P<taskNo>[\w]+)/showPatrolDamage/$', showPatrolDamage, name='showPatrolDamage'),
    url(r'^showPatrolRecord/(?P<taskNo>[\w]+)/showPatrolDamage/showDamage/(?P<damageId>[\d]+)/$', showDamage, name='showDamage'),

    # 讥评巡视模块
    url(r'^showApronRecord/$', showApronRecord, name='showApronRecord'),
    url(r'^showApronRecord/printStandBook/(?P<taskNo>[\w]+)/$', printStandBook, name='printStandBook'),
    url(r'^showApronRecord/printStandBook/(?P<taskNo>[\w]+)/standBook/$', standBook, name='standBook'),
    url(r'^showApronRecord/searchApronPatrolData/$', searchApronPatrolData, name='searchApronPatrolData'),
    url(r'^showApronRecord/addApronPatrolRecord/$', addApronPatrolRecord, name='addApronPatrolRecord'),
    url(r'^showApronRecord/addApronPatrolRecord/addDamageRecord/$', addDamageRecord_apron, name='addDamageRecord_apron'),

    url(r'^showApronRecord/patrolDamageSubmit/$', patrolDamageSubmit_apron, name='patrolDamageSubmit_apron'),
    url(r'^showApronRecord/addApronPatrolRecord/addDamageRecord/receiveDamagePic/$', receiveDamagePic,
        name='receiveDamagePic'),
    url(r'^showApronRecord/patrolRecordSubmit_apron/$', patrolRecordSubmit_apron, name='patrolRecordSubmit_apron'),
]
