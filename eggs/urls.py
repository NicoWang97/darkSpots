# coding: utf-8
"""eggs URL Configuration

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
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from darkSpots import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^upload/',views.upload),
    url(r'^upload_handle/',views.upload_handle),
    url(r'^details',views.details),
    url(r'^upload_success/',views.success),
    url(r'^upload_fail/',views.fail),
    url(r'^data/',views.data), #单张图片的详情页

]

#在urls.py文件最后加上以下内容:

#设置静态文件路径
urlpatterns += staticfiles_urlpatterns()
