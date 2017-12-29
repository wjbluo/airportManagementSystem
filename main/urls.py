from django.conf.urls import url,include
from .views import *
urlpatterns = [
    # 主页模块
    url(r'^$', index, name='index'),

    url(r'^index/$', indexPage, name='IndexPage'),
    url(r'^changeToPdf/$', changeToPdf, name='changeToPdf'),

    # 评价管理
    url(r'^evaluationManagement/', include('evaluationManagement.urls', namespace='evaluationManagement')),

    #道面巡视管理
    url(r'^runwayPatroManagement/', include('runwayPatroManagement.urls', namespace='runwayPatroManagement')),



    # 主页展示  以及 系统管理
    # userManag 用户管理
    url(r'^sysManage/authorization/userManag/$', userManag, name='userManag'),
    url(r'^sysManage/authorization/userManag/addUser/$', addUser, name='addUser'),
    url(r'^sysManage/authorization/userManag/searchUser/$', searchUser, name='searchUser'),
    url(r'^sysManage/authorization/userManag/addUserSubmit/$', addUserSubmit, name='addUserSubmit'),
    url(r'^sysManage/authorization/userManag/frozen/$', frozen, name='frozen'),
    url(r'^sysManage/authorization/userManag/giveRole/(?P<userId>[1-9]+)/$', giveRole, name='giveRole'),
    url(r'^sysManage/authorization/userManag/giveRoleSubmit/$', giveRoleSubmit, name='giveRoleSubmit'),

    # 角色管理
    url(r'^sysManage/authorization/roleManag/$', roleManag, name='roleManag'),
    url(r'^sysManage/authorization/roleManag/searchGroup/$', searchGroup, name='searchGroup'),
    url(r'^sysManage/authorization/roleManag/addGroup/$', addGroup, name='addGroup'),
    url(r'^sysManage/authorization/roleManag/addGroupSubmit/$', addGroupSubmit, name='addGroupSubmit'),
    url(r'^sysManage/authorization/roleManag/lookUsers/(?P<roleId>[0-9]+)/$', lookUsers, name='lookUsers'),
    url(r'^sysManage/authorization/roleManag/givePermission/(?P<roleId>[0-9]+)/$', givePermission, name='givePermission'),
    url(r'^sysManage/authorization/roleManag/givePermissionSubmit/(?P<roleId>[0-9]+)/$', givePermissionSubmit, name='givePermissionSubmit'),

    #基础数据
    #机场基本信息
    url(r'^sysManage/baseData/airportBasicInformation/$', initAirportBasicInformation, name='initAirportBasicInformation'),
    url(r'^sysManage/baseData/airportBasicInformation/alterAirportData/$', alterAirportData, name='alterAirportData'),
    url(r'^sysManage/baseData/airportBasicInformation/alterDataSubmit/$', alterDataSubmit, name='alterDataSubmit'),

    # 跑道信息
    url(r'^sysManage/baseData/runwayBasicInformation/$', initRunwayBasicInformation, name='initRunwayBasicInformation'),
    url(r'^sysManage/baseData/runwayBasicInformation/initRunwayiFrame/$', initRunwayiFrame, name='initRunwayiFrame'),
    url(r'^sysManage/baseData/runwayBasicInformation/addRunwayData/$', addRunwayData, name='addRunwayData'),
    url(r'^sysManage/baseData/runwayBasicInformation/addRunwayDataSubmit/$', addRunwayDataSubmit, name='addRunwayDataSubmit'),
    url(r'^sysManage/baseData/runwayBasicInformation/delRunwayBaseData/$', delRunwayBaseData,
        name='delRunwayBaseData'),
    url(r'^sysManage/baseData/runwayBasicInformation/initRunwayiFrame/alterRunwayData/(?P<runwayId>[0-9]+)/$', alterRunwayData, name='alterRunwayData'),
    url(r'^sysManage/baseData/runwayBasicInformation/alterRunwayDataSubmit/$', alterRunwayDataSubmit,
        name='alterRunwayDataSubmit'),

    # ### # 道面分区
    #部位
    url(r'^sysManage/baseData/roadSurfacePartitionInformation/$', initRoadSurfacePartitionInformation, name='initRoadSurfacePartitionInformation'),
    # url(r'^sysManage/baseData/airportBasicInformation/initSurfacePartitioniFrame/$', initSurfacePartitioniFrame, name='initSurfacePartitioniFrame'),
    url(r'^sysManage/baseData/roadSurfacePartitionInformation/addPart/$', addPart, name='addPart'),
    url(r'^sysManage/baseData/roadSurfacePartitionInformation/addPartSubmit/$', addPartSubmit, name='addPartSubmit'),
    url(r'^sysManage/baseData/roadSurfacePartitionInformation/searchPart/$', searchPart, name='searchPart'),
    url(r'^sysManage/baseData/roadSurfacePartitionInformation/delPartSubmit/$', delPartSubmit, name='delPartSubmit'),
    url(r'^sysManage/baseData/roadSurfacePartitionInformation/alterPart/(?P<partId>[0-9]+)/$',
        alterPart, name='alterPart'),
    url(r'^sysManage/baseData/roadSurfacePartitionInformation/alterPartSubmit/$', alterPartSubmit, name='alterPartSubmit'),
    #区域
    url(r'^sysManage/baseData/roadSurfacePartitionInformation/searchArea/$', searchArea, name='searchArea'),
    url(r'^sysManage/baseData/roadSurfacePartitionInformation/addArea/$', addArea, name='addArea'),
    url(r'^sysManage/baseData/roadSurfacePartitionInformation/addAreaSubmit/$', addAreaSubmit, name='addAreaSubmit'),
    url(r'^sysManage/baseData/roadSurfacePartitionInformation/delAreaSubmit/$', delAreaSubmit, name='delAreaSubmit'),
    url(r'^sysManage/baseData/roadSurfacePartitionInformation/alterArea/(?P<areaId>[0-9]+)/$',
        alterArea, name='alterArea'),
    url(r'^sysManage/baseData/roadSurfacePartitionInformation/alterAreaSubmit/$', alterAreaSubmit,
        name='alterAreaSubmit'),

    #单元
    url(r'^sysManage/baseData/roadSurfacePartitionInformation/initleftMenu/$', initleftMenu,
        name='initleftMenu'),
    url(r'^sysManage/baseData/roadSurfacePartitionInformation/initContent/(?P<areaId>[0-9]+)/$', initContent,
        name='initContent'),
    url(r'^sysManage/baseData/roadSurfacePartitionInformation/searchCell/$', searchCell,
        name='searchCell'),
    url(r'^sysManage/baseData/roadSurfacePartitionInformation/initContent/(?P<areaId>[0-9]+)/addCell/$', addCell, name='addCell'),
    url(r'^sysManage/baseData/roadSurfacePartitionInformation/addCellSubmit/$', addCellSubmit, name='addCellSubmit'),
    url(r'^sysManage/baseData/roadSurfacePartitionInformation/delCellSubmit/$', delCellSubmit, name='delCellSubmit'),
    url(r'^sysManage/baseData/roadSurfacePartitionInformation/initContent/(?P<areaId>[0-9]+)/alterCell/(?P<cellId>[0-9]+)/$', alterCell, name='alterCell'),
    url(r'^sysManage/baseData/roadSurfacePartitionInformation/alterCellSubmit/$', alterCellSubmit,
        name='alterCellSubmit'),

    # 板块
    url(r'^sysManage/baseData/roadSurfacePartitionInformation/initleftMenu_plate/$', initleftMenu_plate,
        name='initleftMenu_plate'),
    url(r'^sysManage/baseData/roadSurfacePartitionInformation/initContent_plate/(?P<cellId>[0-9]+)/$', initContent_plate,
        name='initContent_plate'),
    url(r'^sysManage/baseData/roadSurfacePartitionInformation/searchPlate/$', searchPlate,
        name='searchPlate'),
    url(r'^sysManage/baseData/roadSurfacePartitionInformation/initContent_plate/(?P<cellId>[0-9]+)/addPlate/$', addPlate,
        name='addPlate'),
    url(r'^sysManage/baseData/roadSurfacePartitionInformation/addPlateSubmit/$', addPlateSubmit, name='addPlateSubmit'),
    url(r'^sysManage/baseData/roadSurfacePartitionInformation/delPlateSubmit/$', delPlateSubmit, name='delPlateSubmit'),
    url(r'^sysManage/baseData/roadSurfacePartitionInformation/initContent_plate/(?P<cellId>[0-9]+)/alterPlate/(?P<plateId>[0-9]+)/$',
        alterPlate, name='alterPlate'),
    url(r'^sysManage/baseData/roadSurfacePartitionInformation/alterPlateSubmit/$', alterPlateSubmit,
        name='alterPlateSubmit'),

    # ############道面结构类型
    url(r'^sysManage/baseData/pavementStructureType/$', initPavementStructureType, name='initPavementStructureType'),
    url(r'^sysManage/baseData/pavementStructureType/initStructrueMenu/$', initStructrueMenu,name='initStructrueMenu'),
    url(r'^sysManage/baseData/pavementStructureType/addStructrueCombine/$', addStructrueCombine,name='addStructrueCombine'),
    url(r'^sysManage/baseData/pavementStructureType/addClassSubmit/$', addClassSubmit,name='addClassSubmit'),
    url(r'^sysManage/baseData/pavementStructureType/initStructrueContent/(?P<structureClass>[0-9a-zA-Z\+]+)/(?P<structureCode>[\w]+)/$', initStructrueContent, name='initStructrueContent'),
    url(r'^sysManage/baseData/pavementStructureType/searchLayer/$', searchLayer, name='searchLayer'),
    url(r'^sysManage/baseData/pavementStructureType/initStructrueContent/(?P<structureClass>[0-9a-zA-Z\+]+)/(?P<structureCode>[\w]+)/addLayer/$', addLayer, name='addLayer'),
    url(r'^sysManage/baseData/pavementStructureType/initStructrueContent/(?P<structureClass>[0-9a-zA-Z\+]+)/(?P<structureCode>[\w]+)/showLayerPic/$', showLayerPic,
        name='showLayerPic'),
    url(r'^sysManage/baseData/pavementStructureType/initStructrueContent/(?P<structureClass>[0-9a-zA-Z\+]+)/(?P<structureCode>[\w]+)/alterLayer/(?P<layerId>[0-9]+)/$', alterLayer, name='alterLayer'),
    url(r'^sysManage/baseData/pavementStructureType/alterStructureSubmit/$', alterStructureSubmit,
        name='alterStructureSubmit'),
    url(r'^sysManage/baseData/pavementStructureType/addStructureSubmit/$', addStructureSubmit, name='addStructureSubmit'),
    url(r'^sysManage/baseData/pavementStructureType/delLayerSubmit/$', delLayerSubmit, name='delLayerSubmit'),
    url(r'^sysManage/baseData/pavementStructureType/moveUpLayerSubmit/$', moveUpLayerSubmit, name='moveUpLayerSubmit'),
    url(r'^sysManage/baseData/pavementStructureType/moveDownLayerSubmit/$', moveDownLayerSubmit, name='moveDownLayerSubmit'),


]
