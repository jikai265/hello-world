import json
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from .models import Interfaces
from interfaces.serializers import InterfacesModelSerializer

# Create your views here.
class interfaceView(View):
    """
    1、需要能获取到项目的列数数据（获取多条项目数据或者所有数据）
        url: /interfaces/
        method：GET
        response data: json

    3、能够创建项目（创建一个项目）
        url: /interfaces/
        method：POST
        request data: json
        response data: json
    """
    def get(self, request):
        # a.从数据库中获取所有的项目信息(查询集)
        # obj = InterfacesModelSerializer(instance=Interfaces.objects.all(), many=True)
        # return JsonResponse(obj.data, safe=False)
        qs = Interfaces.objects.all()
        serializer_obj = InterfacesModelSerializer(instance=qs, many=True)
        #serializer_obj = InterfacesModelSerializer()
        # c.向前端返回json格式的数据
        return JsonResponse(serializer_obj.data, status=200, safe=False)


    def post(self, request):
        ret = {
            "msg": "",
            "code": 0
        }
        # a.获取新的项目信息并转化为python中数据类型（字典或者嵌套字典的列表）
        request_data = request.body
        try:
            python_data = json.loads(request_data)
        except Exception as e:
            result = {
                "msg": "参数有误",
                "code": 0
            }
            return JsonResponse(result, status=400)

        serializer_obj1 = InterfacesModelSerializer(data=python_data)
        try:
            serializer_obj1.is_valid(raise_exception=True)
        except Exception as e:
            ret['msg'] = '参数有误'
            ret.update(serializer_obj1.errors)
            return JsonResponse(ret, status=400)

        serializer_obj1.save()

        # d.向前端返回json格式的数据
        ret['msg'] = '成功'
        ret.update(serializer_obj1.data)

        # c.向前端返回json格式的数据
        return JsonResponse(ret, status=201)