from django.conf.urls import url,include
from .views import *
urlpatterns = [
    # 跑滑巡视模块
    url(r'^showPatrolRecord/$', showPatrolRecord, name='showPatrolRecord'),

    url(r'^showPatrolRecord/addPatrolRecord/$', addPatrolRecord, name='addPatrolRecord'),

]
