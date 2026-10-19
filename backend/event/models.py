from django.db import models
from user.models import User


# Create your models here.
class EventType(models.Model):
    '''活动类型表'''
    type_choices = (
        (1, '饮食'),  # 饮食
        (2, '运动'),  # 运动
        (3, '学习'),  # 学习
        (4, '娱乐'),  # 娱乐
        (5, '水果'),  # 水果 健康
        (6, '火锅'),  # 火锅 健康
        (7, '奶茶'),  # 奶茶 健康
        (8, '三餐'),  # 三餐 健康
        (9, '球类'),  # 球类  运动 球 健康
        (10, '跑步'),  # 跑步 好
        (11, '游泳'),  # 游泳 健康
        (12, '瑜伽'),  # 瑜伽 养生
        (13, '英语'),  # 英语 好
        (14, '书法'),  # 书法 好
        (15, '绘画'),  # 绘画
        (16, '读书'),  # 读书 好
        (17, '唱K'),  # 唱K 玩
        (18, '电影'),  # 电影 预告
        (19, '下棋'),  # 下棋 好处
        (20, '轰趴'),  # 轰趴  什么是轰趴
    )
    type = models.IntegerField(verbose_name='活动类型', choices=type_choices)
    tid = models.ForeignKey('self', null=True, blank=True, verbose_name='所属大类')

    def __str__(self):
        return self.get_type_display()

    class Meta:
        verbose_name = '活动类型表'
        verbose_name_plural = '活动类型表'

    # def parent(self):
    #     if self.tid is None:
    #         return ''
    #     else:
    #         pass


class Event(models.Model):
    '''活动信息表'''
    is_deleted_choices = (
        (0, '未删除'),
        (1, '已删除'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_event', verbose_name='发布用户')
    send_time = models.DateTimeField(verbose_name='发布时间', auto_now_add=True)
    content = models.TextField(verbose_name='活动内容')
    type = models.ForeignKey(EventType, on_delete=models.CASCADE, related_name='type_event', verbose_name='活动类型')
    is_deleted = models.IntegerField(verbose_name='删除标记', choices=is_deleted_choices, default=0)

    class Meta:
        verbose_name = '活动表'
        verbose_name_plural = '活动表'
