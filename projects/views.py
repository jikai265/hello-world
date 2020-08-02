import json
import random
import string

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse

from interfaces.models import Interfaces
from .models import Projects
from django.db.models import Q, Count
#from interfaces.models import Interfaces
from .serializers import ProjectsSerializer, ProjectsModelSerializer
#from interfaces.serializers import InterfacesModelSerializer
from django.db import connection  #connection作用：可以在Debug中的watch中添加connection.queries来查看生成的SQL（前提是在DEBUG模式中）
#  Create your views here.


#第一种增删改查并且序列化和反序列化过程

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
    
    前后端是否分离的简单标记：如果后端返回的是一个html页面那就是前后端不分离，如果后端返回的是json格式的数据就是前后端分离
    简单描述两种开发模式的区别？
    在前后端不分离的应用模式中：前端页面看到的效果都是由后端控制，由后端渲染页面或重定向，也就是后端需要控制前端的展示，前端与后端的耦合度很高。
    在前后端分离的应用模式中：后端仅返回前端所需的数据，不再渲染 HTML页面，不再控制前端的效果，至于前端用户看到的什么效果，从后端请求的数据如何加载到前端中，都由前端自己决定，
    网页有网页的处理方式，App由 App的处理方式，但如论那种前端，所需要的数据基本相同，后端仅需开发一套逻辑对外提供数据即可。前端与后端的耦合度相对较低。
    
    两种开发模型：JAVA-MVC和Django-MVT
    Django-MVT:V:处理业务逻辑；M：处理数据，与数据库交互；T:和页面或者用户交互的HTML模板
    Django-MVT流转：客户端发起一个请求到路由表，然后urls.py进行分发，分发之后根据url去调用指定的视图，如果视图需要数据，需要通过模型向数据库请求
                   然后数据库通过模型将数据返回，视图获取到数据，数据需要通过html展示给用户，那么就要通过templates模板引擎渲染成一个合法的HTML页面然后返回到浏览器
    JAVA-MVC和Django-MVT的相通点：
                   1，M全拼是Model,与MVC中的M相同，负责和数据库交互，进行数据处理
                   2，V全拼是View,与MVC中的C相同，接受请求，进行业务处理，返回响应
                   3，T全拼是Templates,与与MVC中的V相同，负责构造要返回的HTML页面
    """

#怎样将html文件通过视图显示到浏览器上
# 1，在专业版中将html页面放在templates目录中（社区版可以自己创建这个目录）
# 2，在settings中的TEMPLATES中添加html文件存放的路径，例如： 'DIRS': [os.path.join(BASE_DIR, 'templates')],
# 3，指定子应用下是否有html页面：'APP_DIRS': True
# 4,index.html中有动态获取data数据的方法，是由django-templates模板引擎帮我们自动将一个html模板语法编译转换为浏览器能够正常打开的页面

class Index(View):#View：它的作用就是对请求进行分发

   #  1、一定要继承View父类，或者View的子类
   #  2、可以定义get、post、put、delete方法，来分别实现GET请求、POST请求、PUT请求、DELETE请求
   #  3、get、post、put、delete方法名称固定，且均为小写

   #例子：怎样将html文件通过视图显示到浏览器上
     # def get(self, request):
     #           # 假设data数据是从数据库读取的
     #           data = [
     #               {
     #                   "project_name": "前程贷项目",
     #                   "leader": "可优",
     #                   "app_name": "P2P平台应用"
     #               },
     #               {
     #                   "project_name": "探索火星项目22",
     #                   "leader": "优优",
     #                   "app_name": "吊炸天应用"
     #               },
     #               {
     #                   "project_name": "无比牛逼的项目33",
     #                   "leader": "可可",
     #                   "app_name": "神秘应用"
     #               },
     #           ]

               # a.render函数主要用于渲染模板生成一个html页面
               # b.第一个参数为request
               # b.第二个参数为在templates目录下的目录名
               # c.第三个参数为context，只能传字典
               #return render(request, 'demo.html')
               #return render(request, 'index.html', locals()) # d.locals()函数能获取当前命名空间中的所有变量信息，然后存放在一个字典中
               # e.JsonResponse是HttpResponse的子类
               # 第一个参数为字典或者嵌套字典的列表，如果为非字典类型，需要将safe设置为False
               # 会返回一个json的字符串
               #return JsonResponse(data, safe=False)  #浏览器加了插件可以显示数据比较友好：JSON-handle

     #def get(self,request): #get没有请求体--boby,其他请求方式都支持boby
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
         #return HttpResponse("<h2>谢谢柠檬班的get老师！</h2>")
         #return render(request,'test.html')

   # 在数据库中随机创建20条数据
    def get(self, request):
          #ascii_letters:大小写字符串，digits：0到9的数字
          one_str = string.ascii_letters + string.digits
          #
          # for i in range(20):
          #     one_list = [random.choice(one_str) for i in range(5)]
          #     one_str_tmp = ''.join(one_list)
          #     one_dict = {
          #         "name": one_str_tmp,
          #         "tester": f"xxx测试0{i}",
          #         "desc": "测试描述",
          #         #"projects_id": random.choice([1, 2, 3])
          #         "leader": f"xxx测试0{i}",
          #         "programmer": f"xxx测试0{i}"
          #     }
          #one_obj = Interfaces.objects.create(**one_dict)
          #one_obj = Projects.objects.create(**one_dict)
          Projects.objects.all()
          return HttpResponse("创建成功！")



     #def post(self,request,pk):
         #注意：在调试的时候，无论传入的是什么数据，都可以在调试窗口通过查看request来定位数据来源和具体数据
         #可以用request.POST去获取application/x-www-form-uriencoded类型的参数
         #可以用request.body去获取json类型的参数；如果传入的参数是其他格式，那么就用对应的模块去处理
         #可以使用request.META方法，获取请求头参数（全都放在字典中），key为HTTP_请求头key的大写 : request.META['HTTP_AUTHORIZATION']
         #data = json.loads(request.body, encoding='utf-8')  #将传过来的json类型的参数转换成python类型的数据（字典），data:{"name":"qingfeng","password":"123456"}
         #return HttpResponse("<h3>post请求，欢迎{}！</h3>".format(data['name']))

    #使用模型类对象进行增删改查
    def post(self,request):
         # 一、创建（C）
         # 1、使用模型类对象来创建
         # 会创建一个Projects模型类对象，但是还未提交
         # project_obj = Projects(name='xxx项目1', leader='xxx项目负责人1',
         #                        tester='xxx测试1', programmer='xxx研发1')
         # 需要调用模型对象的save()方法，去提交
         #project_obj.save()

         # 2、可以使用查询集的create方法
         # objects是manager对象，用于对数据进行操作
         # 使用模型类.objects.create()方法，无需调用save方法(和使用使用模型类对象来创建数据的区别)
         # project_obj = Projects.objects.create(name='xxx项目4', leader='xxx项目负责人4',
         #                                       tester='xxx测试4', programmer='xxx研发4')

         # 二、更新（U）
         # 1、先获取模型类对象，然后修改某些字段，再调用save方法保存
         # project_obj = Projects.objects.get(id=3)   #先查询
         # project_obj.name = '某某知名项目'   #再更新
         # project_obj.save()   #再调用save()才会真正更新

         # 2、可以使用模型类名.objects.filter(字段名=值).update(字段名=修改的值) :直接更新，没有查询，不需要save()
         # one = Projects.objects.filter(id=2).update(name='某某优秀的项目')

         # 三、删除（D）
         # 1、使用模型对象.delete()  :不需要save()
         # project_obj = Projects.objects.get(id=3)
         # project_obj = Projects.objects.all()
         # one = project_obj.delete()

         # 四、查询（C）
         # 使用objects管理器来查询,objects管理器是专门做增删改查的
         # 1、get方法
         # a.一般只能使用主键或者唯一键作为查询条件
         # b.get方法如果查询的记录为空和多条记录，那么会抛出异常
         # c.返回的模型类对象，会自动提交
         #project_obj = Projects.objects.get(id=1)  #方法1

         # Projects.objects.filter(id__gte=2) #方法2，id__gte：意思是>=2
         # Projects.objects.filter()  #正向过滤
         # Projects.objects.exclude()  #饭向过滤

         # 2、all()方法，获取所用记录，支持很多魔术方法
         # a.qs返回QuerySet查询集对象，类似列表的数据,负索引不支持
         # b.查询集对象类似于列表，支持列表中的某些操作
         # c.支持数字索引取值（负索引不支持，返回模型类对象，一条记录）、切片（返回QuerySet查询集对象）
         # d.for循环迭代，每次迭代取出一个模型类对象
         # e.QuerySet查询集对象.first()获取第一个记录、.last()方法获取最后一条记录
         # f.count()方法，获取查询集中数据记录条数
         # g.惰性查询，只有你真正去使用数据时，才会去数据库中执行sql语句，为了性能
         # h.链式调用
         #qs = Projects.objects.all()  #qs[0]模型类对象代表是是数据库中的一条记录
         # 3、filter方法获取特定的某些数量的记录
         # a.filter支持多个过滤表达式，字段名__过滤表达式
         #ws=Projects.objects.filter(name__iendswith="test")
         # b.字段名__startswith、字段名__istartswith（前面加i忽略大小写）：过滤以xxx开头的字符串
         # c.字段名__endswith、字段名__iendswith：过滤以xxx结尾的字符串
         # d.字段名__gt：大于，__gte： >=， __le： <， __lte：<=
         # e.字段名=条件与字段名__exact等价，在Django ORM中有一个内置的变量pk，为数据库模型类的主键别名
         #Projects.objects.filter(name__contains="test"):在查询集中包含"test"
         # f.__contains、__icontains、__in、__isnull
         # g.如果没有指定的记录，会返回空查询集
         #Projects.objects.filter()   #filter()不会像get()那样会抛出异常
         # 4、exclude与filter是反向关系
         # Projects.objects.exclude()

         # 5、关联查询
         # 通过从表的信息获取父表的记录
         # 从表模型类名小写__从表字段名__查询表达式
         # 惰性：查询集对象，只有去使用的时候，才会执行sql语句
         #qs = Interfaces.objects.filter(projects__name__contains="小蓝")  #通过父表的信息获取从表的记录
         #qs = Projects.objects.filter(interfaces__name__regex='^[0-9]')#通过从表的信息获取父表的记录，从表中的name字段以数字开头
         # for item in qs:
         #     print(item.name)

         # 6、逻辑关系查询
         # a.查询集支持链式调用，可以使用filter方法去过滤
         # b.同一行中的多个filter是“与”的关系
         # qs = Projects.objects.filter(name__startswith='x').filter(programmer__contains='4')
         # qs = Projects.objects.filter(name__startswith='x', programmer__contains='4')

         #这里是或的关系处理
         # .filter(Q(查询条件1) | Q(查询条件2))
         # Projects.objects.filter(Q(leader__contains='1') | Q(programmer__contains='4'))

         # 聚合查询
         #Projects.objects.annotate(Count("name"))
         # 7、特殊操作
         # a.使用order_by来进行排序
         # b.可以使用字段名作为排序条件，默认为升序，
         # c.使用-字段名，为降序
         # d.可以同时指定多个排序条件
         # Projects.objects.all().order_by('name')  #升序
         # Projects.objects.all().order_by('-name')  #降序
         # Projects.objects.all().order_by('name'，’-id‘)  #先以name升序再以id降序
         return HttpResponse("<h2>POST请求：欢迎！</h2>")

    def put(self,request):
         #响应数据处理
         # 1.HttpResponse对象，第一个参数为字符串类型或者字节类型，会将字符串内容返回到前端
         # 2.可以使用content_type来指定响应体的内容类型
         # 3.可以使用status参数来指定响应状态码
         # 例子
         # test_dict='{"name":"qingfeng","password":"123456"}'
         # return HttpResponse(test_dict,content_type='application/json',status=205)
         return HttpResponse("<h3>希望柠檬班越办越好！put</h3>")

    def patch(self,request):
         return HttpResponse("<h2>谢谢柠檬班的patch老师！</h2>")



#28日作业

class IndexPage(View):

    """
    类视图
    需求：需要设置5个接口，来提供前端使用对项目的增删改查操作
    1、需要能获取到项目的列数数据（获取多条项目数据或者所有数据）
        url: /projects/
        method：GET
        response data: json

    2、需要能获取到项目的详情数据（获取前端指定某一条数据）
        url: /projects/<int:pk>/
        method：GET
        response data: json

    3、能够创建项目（创建一个项目）
        url: /projects/
        method：POST
        request data: json
        response data: json

    4、能够更新项目（只更新某一个项目）
        url: /projects/<int:pk>/
        method：PUT
        request data: json
        response data: json

    5、能够删除项目（只删除某一个项目）
        url: /projects/<int:pk>/
        method：DELETE

    """

# class ProjectsView(View):
#     """
#     1、需要能获取到项目的列数数据（获取多条项目数据或者所有数据）
#         url: /projects/
#         method：GET
#         response data: json
#
#     3、能够创建项目（创建一个项目）
#         url: /projects/
#         method：POST
#         request data: json
#         response data: json
#     """
#     def get(self, request):  #当从数据库中获取全部数据的时候需要做校验，其他情况都不需要做校验 （这就是一个序列化过程）
#         # a.从数据库中获取所有的项目信息(查询集)
#         qs = Projects.objects.all()
#
#         # b.需要将模型类对象（查询集）转化为嵌套字典的列表
#         python_data = []
#         python_dict = {}
#         for obj in qs:
#             one_dict = {
#                 'id': obj.id,
#                 'name': obj.name,
#                 'leader': obj.leader
#             }
#             python_data.append(one_dict)
#
#         python_dict['msg'] = '获取数据成功'
#         python_dict['code'] = 1
#         python_dict['data'] = python_data
#
#         # c.向前端返回json格式的数据
#         return JsonResponse(python_dict, status=200)
#
#     def post(self, request): #这就是一个反序列化过程
#         # a.获取新的项目信息并转化为python中数据类型（字典或者嵌套字典的列表）
#         request_data = request.body
#         try:
#             python_data = json.loads(request_data)
#         except Exception as e:
#             result = {
#                 "msg": "参数有误",
#                 "code": 0
#             }
#             return JsonResponse(result, status=400)
#
#         # b.校验(非常复杂)
#         if ('name' not in python_data) or ('leader' not in python_data):
#             result = {
#                 "msg": "参数有误",
#                 "code": 0
#             }
#             return JsonResponse(result, status=400)
#
#         # c.创建项目
#         obj = Projects.objects.create(**python_data)
#
#
#
#         # d.向前端返回json格式的数据
#         python_dict = {
#             'id': obj.id,
#             'name': obj.name,
#             'leader': obj.leader,
#             'tester': obj.tester,
#             'programmer': obj.programmer,
#             'code': 1,
#             'msg': '创建成功'
#         }
#
#         # c.向前端返回json格式的数据
#         return JsonResponse(python_dict, status=201)
#
#
# class ProjectDetailView(View):
#     """
#     2、需要能获取到项目的详情数据（获取前端指定某一条数据）
#         url: /projects/<int:pk>/
#         method：GET
#         response data: json
#
#     4、能够更新项目（只更新某一个项目）
#         url: /projects/<int:pk>/
#         method：PUT
#         request data: json
#         response data: json
#
#     5、能够删除项目（只删除某一个项目）
#         url: /projects/<int:pk>/
#         method：DELETE
#     """
#     def get(self, request, pk):
#         # a.校验参数
#         try:
#             obj = Projects.objects.get(id=pk)
#         except Exception as e:
#             result = {
#                 "msg": "参数有误",
#                 "code": 0
#             }
#             return JsonResponse(result, status=400)
#
#         # b.从数据库中获取模型类对象数据
#         python_dict = {
#             'id': obj.id,
#             'name': obj.name,
#             'desc': obj.programmer,
#             'code': 1,
#             'msg': '获取成功'
#         }
#
#         # c.向前端返回json格式的数据
#         return JsonResponse(python_dict)
#
#     def put(self, request, pk):
#         # a.校验pk值并获取待更新的模型类对象
#         try:
#             obj = Projects.objects.get(id=pk)
#         except Exception as e:
#             result = {
#                 "msg": "参数有误",
#                 "code": 0
#             }
#             return JsonResponse(result, status=400)
#
#         # b.获取新的项目信息并校验
#         request_data = request.body
#         try:
#             python_data = json.loads(request_data)
#         except Exception as e:
#             result = {
#                 "msg": "参数有误",
#                 "code": 0
#             }
#             return JsonResponse(result, status=400)
#
#         if ('name' not in python_data) or ('leader' not in python_data):
#             result = {
#                 "msg": "参数有误",
#                 "code": 0
#             }
#             return JsonResponse(result, status=400)
#
#         # c.更新操作
#         obj.name = python_data.get('name') or obj.name  #如果name为空，则将现有的值更新到obj.name中去，等于不更新新的数值
#         obj.leader = python_data.get('leader') or obj.leader
#         obj.tester = python_data.get('tester') or obj.tester
#         obj.programmer = python_data.get('programmer') or obj.programmer
#         obj.desc = python_data.get('desc') or obj.desc
#         obj.save()
#
#         # Projects.objects.filter(id=pk).update(**python_data)
#         # d.向前端返回json格式的数据
#         python_dict = {
#             'id': obj.id,
#             'name': obj.name,
#             'leader': obj.leader,
#             'tester': obj.tester,
#             'code': 1,
#             'msg': '更新成功'
#         }
#
#         # c.向前端返回json格式的数据
#         return JsonResponse(python_dict, status=201)
#
#     def delete(self, request, pk):
#         # a.校验pk值并获取待删除的模型类对象
#         try:
#             obj = Projects.objects.get(id=pk)
#         except Exception as e:
#             result = {
#                 "msg": "参数有误",
#                 "code": 0
#             }
#             return JsonResponse(result, status=400)
#
#         obj.delete()
#
#         python_data = {
#             'msg': '删除成功',
#             'code': 1
#         }
#         return JsonResponse(python_data, status=200)


# summary：
# 上述5个接口的实现步骤：
# 1.数据校验
# 2.将请求信息（json格式的字符串）转化为模型类对象（python中数据类型）
#   a.反序列化：将前端传入的请求参数json类型转换成python数据类型或者python模型类对象
#   b.往往为json格式的字符串（xml）：前端传入的数据类型
#
# 3.数据库操作（创建、更新、获取、删除）
# 4.将模型类对象转化为响应数据（json格式的字符串）返回
#  a.序列化：将模型类对象转化为响应数据（json格式的字符串）返回到前端
#  b.往往为json格式的字符串（xml）
#这里的数据 输入为反序列化过程，输出为序列化过程


# 有哪些痛点：
# 1.代码冗余非常大
# 2.数据校验非常麻烦
# 3.获取列表数据：没有分页操作、过滤操作、排序操作
# 4.不支持以表单来提交参数
# 5.无法自动生成接口文档


#第二种优化过的增删改查并且序列化和反序列化过程
"""
简介：了解DRF框架--REST framework框架：在Django框架基础上进行的二次开发，用于构建Restful Api
特性：
    1，提供了强大的Serializer序列化器，可以高效的进行序列化和反序列化操作
    2，提供了极为丰富的类视图，Mixin扩展类，ViewSet视图集
    3，提供了直观的Web Api界面
    4，多种身份认证和权限认证
    5，强大的排序，过滤，分页，搜索，限流等功能
    6，可扩展性，插件丰富

在客户端和服务器之间发送请求的时候，通过请求头中Content-Type来指明传给服务端的参数类型
                             通过请求头中的Accept来指明希望接受服务端的数据类型

安装及配置：pip install djangorestframefull ;  pip install markdown
在setting中的INSTALLED_APPS添加'rest_framework',
"""
from .serializers import ProjectsSerializer

# ret = {
#         "msg": "",
#         "code": 0
# }


# 序列化器对象中的几个重要属性
# 一、一定要先执行.is_valid()方法之后才能访问
# .errors 获取报错信息
# .validated_data 校验通过之后的数据（往往也是数据库中需要保存的数据）

# 二、可以不用调用.is_valid()方法，也能访问
# .data 最终返回给前端的数据

class ProjectsView(View):
    """
    1、需要能获取到项目的列数数据（获取多条项目数据或者所有数据）
        url: /projects/
        method：GET
        response data: json

    3、能够创建项目（创建一个项目）
        url: /projects/
        method：POST
        request data: json
        response data: json
    """
    def get(self, request):
        # a.从数据库中获取所有的项目信息(查询集)
        #qs = Projects.objects.all()

        # b.需要将模型类对象（查询集）转化为嵌套字典的列表
        # python_data = []
        # python_dict = {}
        # for obj in qs:
        #     one_dict = {
        #         'id': obj.id,
        #         'name': obj.name,
        #         'leader': obj.leader
        #     }
        #     python_data.append(one_dict)
        #
        # python_dict['msg'] = '获取数据成功'
        # python_dict['code'] = 1
        # python_dict['data'] = python_data

        # 1.可以使用序列化器类来进行序列化输出
        # a.instance参数可以传模型类对象
        # b.instance参数可以传查询集（多条记录），many=True
        # c.可以ProjectsSerializer序列化器对象，调用data属性，可以将模型类对象转化为Python中的数据类型
        # d.如果未传递many=True参数，那么序列化器对象.data，返回字典，否则返回一个嵌套字典的列表（也就是返回多条数据）
        #serializer_obj = ProjectsSerializer(instance=qs, many=True)
        #***********
        #使用序列化器类来生成序列化字段
        qs = Projects.objects.all()
        serializer_obj = ProjectsModelSerializer(instance=qs, many=True)
        #serializer_obj = ProjectsModelSerializer()
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

        # b.校验(非常复杂)
        # if ('name' not in python_data) or ('leader' not in python_data):
        #     result = {
        #         "msg": "参数有误",
        #         "code": 0
        #     }
        #     return JsonResponse(result, status=400)

        #使用序列化器进行校验
        # 1、创建序列化器对象
        # a.把前端传递的json格式参数转化为字典之后，传递给data参数
        # b.序列化器对象.is_valid()方法，开始进行校验，如果不调用此方法，那么不会进行校验
        # c.调用序列化器对象.is_valid()方法，如果校验成功，返回True，否则返回False
        # d.必须调用is_valid()方法之后，才能使用.errors属性去获取报错信息，相当于一个字典
        # e.必须调用is_valid()方法之后，才能使用.validated_data属性去获取校验通过信息，相当于一个字典

        # 在定义序列化器对象时，只给data传参
        #a,使用序列化器对象save()，会自动调用序列化器类中的create方法
        #serializer_obj1 = ProjectsSerializer(data=python_data)
        serializer_obj1 = ProjectsModelSerializer(data=python_data)
        try:
            serializer_obj1.is_valid(raise_exception=True)  #raise_exception=True：校验失败后抛出异常
        except Exception as e:
            ret['msg'] = '参数有误'
            ret.update(serializer_obj1.errors)
            return JsonResponse(ret, status=400)

        # if not serializer_obj1.is_valid():
        #     ret['msg'] = '参数有误'
        #     ret.update(serializer_obj1.errors)
        #     return JsonResponse(ret, status=400)

        # c.创建项目
        #obj = Projects.objects.create(**ret)
        #obj=Projects.objects.create(**serializer_obj1.validated_data) #validated_data属性用来获取校验通过信息，相当于一个字典

        # d.向前端返回json格式的数据
        # python_dict = {
        #     'id': obj.id,
        #     'name': obj.name,
        #     'leader': obj.leader,
        #     'tester': obj.tester,
        #     'programmer': obj.programmer,
        #     'code': 1,
        #     'msg': '创建成功'
        # }
        #serializer_obj1 = ProjectsSerializer(instance=obj)
        # 在调用save方法时，传递的关键字参数，会自动添加到create()方法，validated_data字典中
        serializer_obj1.save()

        ret['msg'] = '成功'
        #ret.update(serializer_obj1.validated_data)
        ret.update(serializer_obj1.data)   #最终返回给前端的数据

        # c.向前端返回json格式的数据
        #return JsonResponse(serializer_obj1.data, status=201)
        return JsonResponse(ret, status=201)


class ProjectDetailView(View):
    """
    2、需要能获取到项目的详情数据（获取前端指定某一条数据）
        url: /projects/<int:pk>/
        method：GET
        response data: json

    4、能够更新项目（只更新某一个项目）
        url: /projects/<int:pk>/
        method：PUT
        request data: json
        response data: json

    5、能够删除项目（只删除某一个项目）
        url: /projects/<int:pk>/
        method：DELETE
    """

    def get_object(self, pk):  #提取查询记录的方法
        try:
            obj = Projects.objects.get(id=pk)
        except Exception as e:
            result = {
                "msg": "参数有误",
                "code": 0
            }
            return JsonResponse(result, status=400)
        return obj


    def get(self, request, pk):
        # a.校验参数
        # try:
        #     obj = Projects.objects.get(id=pk)
        # except Exception as e:
        #     result = {
        #         "msg": "参数有误",
        #         "code": 0
        #     }
        #     return JsonResponse(result, status=400)
        obj=self.get_object(pk)
        # b.从数据库中获取模型类对象数据-旧
        # python_dict = {
        #     'id': obj.id,
        #     'name': obj.name,
        #     'desc': obj.programmer,
        #     'create_time': obj.create_time,
        #     'code': 1,
        #     'msg': '获取成功'
        # }
        #serializer_obj：序列化器类对象
        #serializer_obj = ProjectsSerializer(instance=obj)  #优化过后
        serializer_obj = ProjectsModelSerializer(instance=obj)  # 使用模型序列化类实现
        #python_dict = serializer_obj.data  #返回的是字典（一条数据）

        # c.向前端返回json格式的数据
        return JsonResponse(serializer_obj.data)

    def put(self, request, pk):
        ret = {
            "msg": "",
            "code": 0
        }

        # a.校验pk值并获取待更新的模型类对象
        # try:
        #     obj = Projects.objects.get(id=pk)
        # except Exception as e:
        #     result = {
        #         "msg": "参数有误",
        #         "code": 0
        #     }
        #     return JsonResponse(result, status=400)
        obj=self.get_object(pk)
        # b.获取新的项目信息并校验
        request_data = request.body
        try:
            python_data = json.loads(request_data)
        except Exception as e:
            result = {
                "msg": "参数有误",
                "code": 0
            }
            return JsonResponse(result, status=400)

        # if ('name' not in python_data) or ('leader' not in python_data):
        #     result = {
        #         "msg": "参数有误",
        #         "code": 0
        #     }
        #    return JsonResponse(result, status=400)


        # 如果在定义序列化器对象时，同时指定instance和data参数
        # a.调用序列化器对象.save()方法，会自动调用序列化器类中的update方法
        #serializer_obj1 = ProjectsSerializer(instance=obj, data=python_data)
        serializer_obj1 = ProjectsModelSerializer(instance=obj, data=python_data)
        try:
            serializer_obj1.is_valid(raise_exception=True)
        except Exception as e:
            ret['msg'] = '参数有误'
            ret.update(serializer_obj1.errors)
            return JsonResponse(ret, status=400)

        # c.更新操作1
        # obj.name = serializer_obj1.validated_data.get('name') or obj.name  ,校验之后的数据更新
        # obj.name = python_data.get('name') or obj.name  ,校验之前的数据更新
        # obj.leader = python_data.get('leader') or obj.leader
        # obj.tester = python_data.get('tester') or obj.tester
        # obj.programmer = python_data.get('programmer') or obj.programmer
        # obj.desc = python_data.get('desc') or obj.desc
        # obj.save()

        # Projects.objects.filter(id=pk).update(**python_data) #更新操作2
        # d.向前端返回json格式的数据
        # python_dict = {
        #     'id': obj.id,
        #     'name': obj.name,
        #     'leader': obj.leader,
        #     'tester': obj.tester,
        #     'code': 1,
        #     'msg': '更新成功'
        # }
        serializer_obj1.save()  #这一步会自动调用序列化器类中的create方法
        #serializer_obj1.save(user="清风")  # 这一步会是清风创建的
        #serializer_obj = ProjectsSerializer(instance=obj)


        # c.向前端返回json格式的数据
        return JsonResponse(serializer_obj1.data, status=201)


    def delete(self, request, pk):
        # a.校验pk值并获取待删除的模型类对象
        # try:
        #     obj = Projects.objects.get(id=pk)
        # except Exception as e:
        #     result = {
        #         "msg": "参数有误",
        #         "code": 0
        #     }
        #     return JsonResponse(result, status=400)
        obj = self.get_object(pk)
        obj.delete()

        python_data = {
            'msg': '删除成功',
            'code': 1
        }
        return JsonResponse(python_data, status=200)