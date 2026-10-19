from django.db import models

# Create your models here.


class MessageLog(models.Model):
    fromuser = models.CharField(verbose_name="发送方", max_length=100, null=False)
    touser = models.CharField(verbose_name='接收方', max_length=100, null=False)
    content = models.CharField(verbose_name="消息", max_length=100, null=False)
    # requiredText = ((0, '是'), (1, '否'))
    # is_required = models.IntegerField(verbose_name='是否已读', choices=requiredText, default=0)
    create_time = models.DateTimeField(verbose_name='创建时间')  # auto_now_add：取新增时候的时间
    send_choices = ((0, '未发送'), (1, '已发送'))
    is_send = models.IntegerField(verbose_name='是否发送', choices=send_choices)

    class Meta:
        verbose_name = '聊天记录表'
        verbose_name_plural = '聊天记录表'
