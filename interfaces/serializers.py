
from rest_framework import serializers
from rest_framework import validators

#from projects.serializers import ProjectsModelSerializer
from .models import Interfaces
from projects.models import Projects
#from projects.serializers import ProjectsModelSerializer


# 使用模型序列化器类：简化序列化器类中字段的创建
class InterfacesModelSerializer(serializers.ModelSerializer):
    # 通过子表获取父表的信息
    # a.会将父表的主键id值作为返回值
    # projects = serializers.PrimaryKeyRelatedField(help_text='所属项目', label='所属项目', queryset=Projects.objects.all())
    # b.会将父表对应对象的__str__方法的结果返回,也就是从表中的projects_id对应父表的name值
    projects = serializers.StringRelatedField(many=True)
    # c.会将父表对应对象的某个字段的值返回，返回值变量要和Interfaces中的外键表字段一致，这里就是projects
    #projects = serializers.SlugRelatedField(slug_field='leader', read_only=True)
    # d.可以将某个序列化器对象定义为字段，支持Field中的所有参数
    #projects = ProjectsModelSerializer(label='所属项目信息', help_text='所属项目信息', read_only=True)

    class Meta:
        model = Interfaces
        # fields = ('id', 'name', 'leader', 'tester', 'programmer', 'create_time', 'update_time', 'email')
        fields = '__all__'

    def create(self, validated_data):   #前端传递进来项目id会通过create转化成模型类对象
        # Interfaces(name='', projects=obj)
        pass
