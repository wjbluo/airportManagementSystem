from django.conf.urls import url,include
from .views import *
urlpatterns = [
    # 登录模块
    url(r'^login/$', login, name='login'),
    url(r'^create_code_img/', create_code_img,name='create_code_img'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^modifyPwd/$', modifyPwd, name='modifyPwd'),
    url(r'^modifyPsdSubmit/$', modifyPsdSubmit, name='modifyPsdSubmit')
]
