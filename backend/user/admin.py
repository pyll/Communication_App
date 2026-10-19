from django.contrib import admin
from user.models import *


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'password', 'gender', 'school']
    ordering = ('id',)

    class Meta:
        verbose_name = '用户表'
        verbose_name_plural = '用户表'


@admin.register(UserToken)
class UserToken(admin.ModelAdmin):
    list_display = ['id', 'token', 'user']
    ordering = ('id',)


