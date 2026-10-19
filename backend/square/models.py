from django.db import models
from user.models import User

# Create your models here.
class Square(models.Model):
    '''
    广场表
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_square')
    content = models.TextField(verbose_name='广场内容')
    send_time = models.DateTimeField(verbose_name='发布时间', auto_now_add=True)

    class Meta:
        verbose_name = '动态表'
        verbose_name_plural = '动态表'
