from django.db import models
#对象关系映射(英语:(Object Relational Mapping，简称ORM，或O/RM，或O/R mapping)，是一种程序技术，
#用于实现面向对象编程语言里不同类型系统的数据之间的转换 。从效果上说，它其实是创建了一个可在编程语言里使用的--"虚拟对象数据库"。

# Create your models here.
#数据库信息要在settings中的DATABASES进行配置

# 一个mysql软件中，可以有多个数据库
# 一个数据库中，可以有多张数据表
# 一张数据表中，有多条数据（多条记录）以及多个字段（多个列）

# 1、可以在子应用projects/models.py文件中，来定义数据模型
# 2、一个数据模型类对应一个数据表
# 3、数据模型类，需要继承Model父类或者Model子类
# 4、在数据模型类中，添加的类属性（Field对象）来对应数据表中的字段
# 5、创建完数据库模型类之后，需要迁移才能生成数据表
#    a.生成迁移脚本，放在projects/migrations目录中：python manage.py makemigrations
#    b.执行迁移脚本：python manage.py migrate  注意：迁移失败的时候要把历史信息删除再迁移就会成功
       #1,python manage.py showmigrations projects :显示子项目projects下的迁移脚本
       #2,python manage.py sqlmigrate projects 0001_initial :显示子项目projects下的迁移脚本做了哪些SQL操作
#    c.如果不添加选项，那么会将所有子应用进行迁移
# 6、会自动创建字段名为id的类属性，自增、主键（primary_key）、非空
# AutoField: 自增长类型，映射到数据库中是11位的整数，使用此字段时，必须传递primary_key = True，否则在生成迁移脚本文件时就会报错，一个模型不能有两个自增长字段。
             #一般情况下我们用不到这个字段，如果不定义主键，django会自动的为我们生成id字段作为主键
class Projects(models.Model):  #模型类
    # 7、只要某一个字段中primary_key=True，那么Django就不会自动创建id字段，会使用自定义的
    # 8、CharField -> varchar
    # IntegerField -> int
    # TextField -> text
    id = models.AutoField(primary_key=True)
    # 9、verbose_name：为个性化信息，相当于给这个字段添加一个中文提示
    # 10、help_text：帮助文本信息，说明字段的含义，在api接口文档平台和admin后端站点中会用于提示，往往跟verbose_name一致
    # 11、unique：在表中这个字段的值是否唯一，在数据库中就是唯一约束，一般是设置手机号码/邮箱等，默认为False
    # 12、CharField：至少要指定一个max_length必传参数，代表此字段的最大长度，不能为负数
    #models.IntegerField() #empty_strings_allowed = False，代表如果传值为空是不被允许的，如果是empty_strings_allowed = Ture,则默认传一个空字符串进来
    name = models.CharField(max_length=200, verbose_name='项目名称', help_text='项目名称', unique=True)
    leader = models.CharField(max_length=50, verbose_name='项目负责人', help_text='项目负责人')
    tester = models.CharField(max_length=50, verbose_name='测试人员', help_text='测试人员')
    programmer = models.CharField(max_length=50, verbose_name='开发人员', help_text='开发人员')
    # 13、null指定数据在数据库保存时是否可以为空，默认不能为空，如果null=True，那么可以为空值
    # 14、blank指定前端用户在创建数据时，是否需要传递，默认需要传递，如果不传递，需要blank设置为True，那我们就用default传一个默认值，这个字段往往和null一起使用，models中的blank，只在生成序列化器字段时生效，单独创建模型对象，无效
         #注意:blank和null只有针对序列化器的时候才起作用，对于类似Projects.objects.create（）的操作并没有做限制，主要是要看empty_strings_allowed = False还是Ture来决定的，还有就是针对from表单也起作用
    # 15、default为某一个字段指定默认值，往往会跟blank一起使用，如果在保存数据时不为空并且前端用户在创建数据时可以不传参数，那么就要指定一个默认值(只有发起请求的时候才起作用)
    # 16，db_column：这个字段在数据库中的名字。如果没有设置这个参数，那么将会使用模型中属性的名字。
    # 17，db_index：标识这个字段是否为索引字段。
    desc = models.TextField(verbose_name='项目简介', help_text='项目简介', blank=True, default='xxx简介',null=True)

    # 16、DateTimeField可以添加auto_now_add选项，django会自动添加创建记录时的时间
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    # 17、DateTimeField可以添加auto_now选项，django会自动添加更新记录时的时间,只有在视图调用save()的时候才会更新
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text='更新时间')

    # 18、执行迁移脚本之后，生成的数据表名默认为: 子应用名_模型类名小写

    class Meta:
        # 19、可以在模型类下定义Meta子类，Meta子类名称固定
        # 20、可以使用db_table类属性，来指定表名
        db_table = 'tb_projects'
        # 21、verbose_name指定表的个性化描述
        verbose_name = '项目表'

    def __str__(self):  #在我们打印返回数据的时候自动返回字符串
        return f"<{self.name}>"  #将项目的名称作为返回值