#文件名可以不使用serializers，但是通常都会这么命名

from rest_framework import serializers
from rest_framework import validators  #唯一性校验

from .models import Projects

# value是前端输入的待校验的值,也可以自定义别的名称
def is_name_contain_x(value):
    # 如果校验失败，一定要抛出ValidationError异常类对象，第一个参数可以指定具体的报错信息
    if 'x' in value:
        raise serializers.ValidationError("项目名称中不能包含x")

class ProjectsSerializer(serializers.Serializer):
    """""
    serializers的作用：可以定义序列化器类，来实现序列化和反序列化操作
    a.一定要继承serializers.Serializer或者Serializer的子类
    b.默认情况下，可以定义序列化器字段，序列化器字段名要与模型类中字段名相同
    c.默认情况下，定义几个序列化器字段，那么就必须返回几个数据（到前端，序列化输出的过程）否则会报错，前端也必须得传递这几个字段（反序列化过程）
    d.在serializers中定义的字段一定要和models中定义的字段一致
    """""
    # 校验顺序
    # a.字段定义时的校验（校验参数 -> validators参数校验列表） -> 进行单字段的校验 -> 进行多字段联合校验

    # d.CharField、BooleanField、IntegerField与模型类中的字段类型一一对应
    # e.required参数默认为None，指定前端必须得传此字段，如果设置为False的话，前端可以不传此字段
    # f.label和help_text -> verbose_name和help_text一一对应
    # g.allow_null指定前端传递参数时可以传空值
    # CharField字段，max_length指定该字段不能操作的字节参数，

    #使用validators参数，可以指定校验规则
    #校验规则：
    #a,DRF自带的校验规则UniqueValidator，第一个参数是查询集（我们当前项目名称所处的查询集），第二个参数是校验失败之后的报错信息
    #b，自定义的校验规则
    #c, validators列表中的校验规则，会全部执行校验
    name = serializers.CharField(max_length=10, label='项目名称', help_text='项目名称', min_length=2,
                                 validators=[validators.UniqueValidator(queryset=Projects.objects.all(), message='项目已存在'), is_name_contain_x]) #validators：重复项目检验
    # leader = serializers.CharField(max_length=200, label='项目负责人', help_text='项目负责人')
    # h.如果某个字段指定read_only=True，那么此字段，前端在创建数据时（反序列化过程）可以不用传，但是一定会输出（序列化过程）
    # i.字段不能同时指定read_only=True, required=True
    # leader = serializers.CharField(max_length=200, label='项目负责人', help_text='项目负责人', read_only=True, required=True)
    leader = serializers.CharField(max_length=200, label='项目负责人', help_text='项目负责人', read_only=True)
    # tester = serializers.CharField(max_length=200, label='测试人员', help_text='测试人员')
    # j.如果某个字段指定write_only=True，那么此字段只能进行反序列化输入，而不会输出（创建数据时必须得传，但是不返回）
    # k.可以给字段添加error_messages参数，为字典类型，字典的key为校验的参数名，值为校验失败之后错误提示
    tester = serializers.CharField(max_length=200, label='测试人员', help_text='测试人员', write_only=True,
                                   error_messages={"required": "该字段必传1", "max_length": "长度不能操作200个字节"})
    # k.一个字段不同同时指定write_only=True, read_only=True
    # tester = serializers.CharField(max_length=200, label='测试人员', help_text='测试人员', write_only=True, read_only=True)


    # 在序列化器类中对单字段进行校验，不需要添加到validators中
    # a.必须要以validate_作为前缀
    # b.校验方法名称为：validate_字段名
    # c.一定要返回校验成功之后的值，外边定义的可以不返回
    def validate_name(self, value):
        if '非常' in value:
            raise serializers.ValidationError("项目名称中不能包含‘非常’")
        return value

    # 在序列化器类中对多字段进行联合校验
    # a.校验方法的固定名称为：validate
    # b.一定要返回校验成功之后的值
    # c.attrs为前端输入的待校验参数
    def validate(self, attrs):   #attrs是字典
        if len(attrs['name']) != 8 or '测试' not in attrs['tester']:
            raise serializers.ValidationError("项目名长度不为8或者测试人员名称中不包含'测试'")  #多字段联合校验的时候报错会返回一个非定义字段（指的是在serializers中定义的字段）:non_field_errors
                                                                                        #在源码当中有一个修改全局参数的地方：DRF中的setting.py中有一个non_field_errors_KEY的键，在DEV04中的
        return attrs                                                                    #setting.py中加入REST_FRAMEWORK = { 'NON_FIELD_ERRORS_KEY': 'errors',}来解决


    def create(self, validated_data):
        # validated_data参数为校验通过之后的数据
        # 必须将创建成功的模型类对象返回
        obj = Projects.objects.create(**validated_data)
        return obj

    def update(self, instance, validated_data):
        # instance为待更新的模型类对象
        # validated_data参数为校验通过之后的数据
        # 必须将更新成功的模型类对象返回
        instance.name = validated_data.get('name') or instance.name
        instance.leader = validated_data.get('leader') or instance.leader
        instance.tester = validated_data.get('tester') or instance.tester
        instance.programmer = validated_data.get('programmer') or instance.programmer
        instance.desc = validated_data.get('desc') or instance.desc
        instance.save()
        return instance