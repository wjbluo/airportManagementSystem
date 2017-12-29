"""airportManagementSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.conf import settings
from django.views import static

favicon_view = RedirectView.as_view(url='/static/darkgrey/images/bitbug_favicon.ico', permanent=True)

urlpatterns = [
    url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT }, name='static'),

    url(r'^admin/', admin.site.urls),
    #icon设置
    url(r'^favicon\.ico$', favicon_view),

    # 用户登录模块
    url(r'^account/', include('login.urls',namespace='account')),

    # 主页展示  以及 系统管理
    url(r'^component/', include('main.urls', namespace='sysManage')),

]

