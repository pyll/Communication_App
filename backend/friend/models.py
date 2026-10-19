from django.db import models
from user.models import User

# Create your models here.


class Friend(models.Model):
    '''
    好友表
    '''
    is_deleted_choices = (
        (0, '未删除'),
        (1, '删除'),
    )
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_friend1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_friend2')
    is_deleted = models.IntegerField(verbose_name='删除标记', choices=is_deleted_choices, default=0)

    class Meta:
        verbose_name = '好友表'
        verbose_name_plural = '好友表'


class FriendLog(models.Model):
    '''
    好友信息处理表
    '''
    is_agreed_choices = (
        (0, '未同意'),
        (1, '已同意'),
        (2, '拒绝'),
    )
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_friendlog1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_friendlog2')
    is_agreed = models.IntegerField(verbose_name='同意标记', choices=is_agreed_choices, default=0)

    class Meta:
        verbose_name = '好友日志表'
        verbose_name_plural = '好友日志表'
