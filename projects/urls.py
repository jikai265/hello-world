"""projects URL Configuration

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
from django.urls import path
from projects.views import index_page, index_page1, Index, IndexPage, ProjectsView, ProjectDetailView  # 例子1
from interfaces.views import interfaceView

urlpatterns = [
    #path('projects/', index_page1),
    path('projects1/<int:pk>/', Index.as_view()),#可以使用<url类型转化器:路径参数名>; <>是路径转换器，这里一定要传入int类型并且会讲参数赋值给id
                                               #在DJANGO中还有int、path、uuid、slug等等类型转换器
    path('projects/', Index.as_view()),# as_view：这个是有view的父类dispatch方法去分发实现的
    path('IndexPage/', IndexPage.as_view()),
    path('ProjectsView/', ProjectsView.as_view()),
    path('ProjectDetailView/<int:pk>/', ProjectDetailView.as_view()),
    path('interfaceView/', interfaceView.as_view()),
    #path('ProjectDetailView/<int:pk>/', ProjectDetailView.as_view()),

]
