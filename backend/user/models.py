from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    # username = models.CharField(max_length=150, unique=True)
    # password = models.CharField(max_length=128)
    # date_joined = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    gender_choices = (
        (0, '男'),
        (1, '女'),
    )
    # phone = models.CharField(max_length=11, verbose_name='手机号')
    avatar = models.CharField(max_length=254, verbose_name='用户头像url')
    school = models.CharField(max_length=100, verbose_name='学校')
    gender = models.IntegerField(verbose_name='性别', choices=gender_choices, default=0)
    # student_id = models.CharField(max_length=128, verbose_name='学生学号')
    birth = models.DateField(verbose_name='出生日期', null=True)
    major = models.CharField(max_length=128, verbose_name='专业')
    like = models.CharField(max_length=254, verbose_name='喜欢的动态类型')

    class Meta:
        verbose_name = '用户表'
        verbose_name_plural = '用户表'


class UserToken(models.Model):
    user = models.OneToOneField(to='User', on_delete=models.CASCADE)
    token = models.CharField(max_length=64)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now=True)

    class Meta:
        verbose_name = 'token表'
        verbose_name_plural = 'token表'

