import json
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
#  Create your views here.


# 例子1
def index_page(request):  # request：第一个参数是HTTPRequest对象或HTTPRequest子类的对象,无需手动传递，request相当于所有前端参数封装的对象，通过这个对象
                          # 可以获取到前端传递过来的任何参数
    return HttpResponse('你好，Django！')   #只要是视图函数就必须要返回一个HttpResponse对象或HttpResponse子类的对象

# 例子2 函数视图
def index_page1(request):
    if request.method=="GET":
        return HttpResponse("<h2>谢谢柠檬班的get老师！</h2>")
    elif request.method=="POST":
         return HttpResponse("<h3>希望柠檬班越办越好！post</h3>")
    elif request.method == "PUT":
        return HttpResponse("<h3>希望柠檬班越办越好！put</h3>")
    else:
        return HttpResponse("<h3>其他请求</h3>")
    """
# 例子3,类视图
    类视图
    1、一定要继承View父类，或者View的子类
    2、可以定义get、post、put、delete方法，来分别实现GET请求、POST请求、PUT请求、DELETE请求
    3、get、post、put、delete方法名称固定，且均为小写
    4、实例方法的第二个参数为HttpRequest对象
    5、一定要返回HttpResponse对象或者HttpResponse子类对象
    6、json数据的分类：json对象和json数组，json当中所有的key都是双引号

         jsonObject:
         "Row": {
             "YLX": "2010",
             "ZYY": "变更",
             "YWH": "60000000020181213",
             "JYH": "200151"
         }

         jsonArray:
         "Row": [
             {
                 "YWX": "200",
                 "ZYY": "变更",
                 "YBH": "60000000020181213,
                        "JYH":"200151"
         }
         ]
         
    http://127.0.0.1:8000/projects/?name=test&pssword=123456 :?号后面的参数称为查询字符串参数
    在类视图中如何处理查询字符串参数？
    方案：见类视图中的get说明
    
    """
class Index(View):#View：它的作用就是对请求进行分发

   #  1、一定要继承View父类，或者View的子类
   #  2、可以定义get、post、put、delete方法，来分别实现GET请求、POST请求、PUT请求、DELETE请求
   #  3、get、post、put、delete方法名称固定，且均为小写


     def get(self,request): #get没有请求体--boby,其他请求方式都支持boby
         # 实例方法的第一个参数self是类Index的实例对象，第二个参数request为HttpRequest对象或者HttpRequest子类对象
         # 一定要返回HttpResponse对象或者HttpResponse子类对象
         # 如果想要显示一个请求的所有属性可以使用dir()来实现，例如dir(request.GET)
         # http://127.0.0.1:8000/projects/?name=test&pssword=123456 :
         # url后面的？号参数，称为query string查询字符串参数 ?参数名1=参数值1&参数名2=参数值2
         # request.GET去获取查询字符串参数
         # request.GET返回一个请求字典--QueryDict对象，支持字典中的所有操作
         # request.GET[key]；request.GET.get(key)；request.GET.getlist()去获取多个参数值，例如：request.GET.getlist(‘key’)
         #在postman中fromdata和x-www-form-uriencoded都属于from表单类型数据，区别在于x-www-form-uriencoded进行了uriencoded编码,表单中还可以选择文件
         #类型参数
         #json格式在postman中的row中选择添加
         return HttpResponse("<h2>谢谢柠檬班的get老师！</h2>")
         #return render(request,'test.html')

     def post(self,request):
         #注意：再调试的时候，无论传入的是什么数据，都可以在调试窗口通过查看request来定位数据来源和具体数据
         #可以用request.POST去获取application/x-www-form-uriencoded类型的参数
         #可以用request.body去获取json类型的参数；如果传入的参数是其他格式，那么就用对应的模块去处理
         #可以使用request.META方法，获取请求头参数（全都放在字典中），key为HTTP_请求头key的大写 : request.META['HTTP_AUTHORIZATION']
         data = json.loads(request.body, encoding='utf-8')  #将传过来的json类型的参数转换成python类型的数据（字典），data:{"name":"qingfeng","password":"123456"}
         #print(data)

         return HttpResponse("<h3>post请求，欢迎{}！</h3>".format(data['name']))

     def put(self,request):
         return HttpResponse("<h3>希望柠檬班越办越好！put</h3>")

     def patch(self,request):
         return HttpResponse("<h2>谢谢柠檬班的patch老师！</h2>")