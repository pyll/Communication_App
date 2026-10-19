from rest_framework import serializers
from user.models import User, UserToken
from event.models import Event, EventType
from datetime import datetime
from qiniu import Auth, put_file, etag
from user.utils.config import configs
import time


# ModelSerializer 比Serializer封装好了一层，直接自己生成的create和update，不用覆盖了，其实推荐用Serializer
class RegisterSerializer(serializers.ModelSerializer):
    '''
    注册
    '''
    class Meta:
        model = User
        fields = ('username', 'password', 'school', 'gender', 'avatar')
        # fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source="get_gender_display")

    class Meta:
        model = User
        fields = ('username', 'password', 'school', 'gender', 'avatar', 'birth', 'major')  #
        # fields = '__all__'


class FriendSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source="get_gender_display")

    class Meta:
        model = User
        fields = ('username', 'school', 'gender', 'avatar', 'birth', 'major')  #
        # fields = '__all__'

