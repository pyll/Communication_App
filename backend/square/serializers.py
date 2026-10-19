from rest_framework import serializers
from square.models import *

# ModelSerializer 比Serializer封装好了一层，直接自己生成的create和update，不用覆盖了，其实推荐用Serializer


# 上面的另一种写法
class SquareSerializer(serializers.ModelSerializer):
    send_time = serializers.SerializerMethodField()  # 对应get_send_time方法
    username = serializers.CharField(source='user.username')
    school = serializers.CharField(source='user.school')
    gender = serializers.CharField(source='user.get_gender_display')

    # 自定义字段, get_开头.字段名结尾
    def get_send_time(self, row):
        return row.send_time.strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Square
        fields = ['id', 'send_time', 'username', 'content', 'school', 'gender']
        # fields = '__all__'
