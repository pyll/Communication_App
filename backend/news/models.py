from django.db import models

# Create your models here.
class News(models.Model):
    '''
    资讯表
    '''
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

    title = models.CharField(max_length=200, verbose_name='标题')
    author = models.CharField(max_length=100, verbose_name='作者')
    time = models.DateTimeField(verbose_name='发布时间')
    content = models.TextField(verbose_name='内容')
    type = models.IntegerField(verbose_name='类型id', choices=type_choices)

    class Meta:
        verbose_name = '资讯表'
        verbose_name_plural = '资讯表'
