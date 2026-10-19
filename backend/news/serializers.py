from rest_framework import serializers
from news.models import News


class EachNewsSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type_display')  # type
    time = serializers.SerializerMethodField()
    # type = serializers.SerializerMethodField()

    # 自定义字段, get_开头.字段名结尾
    def get_time(self, row):
        return row.time.strftime('%Y-%m-%d %H:%M')

    class Meta:
        model = News
        fields = '__all__'
        # fields = ['id', 'type', 'time', 'content', 'author', 'title']

