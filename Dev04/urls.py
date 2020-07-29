"""Dev04 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include #访问子路由地址时，必须在主路由中导入include并添加：path('page/', include('子项目.urls')),系统会先到主路由中匹配到include则系统会继续在子路由中寻找对应的路由信息
#from projects.views import index_page #例子1

urlpatterns = [
    path('admin/', admin.site.urls),
    path('page/', include('projects.urls')),
    #path('index/', index_page), #例子1
    #path('index/<int:pk>/', index_page),
]
