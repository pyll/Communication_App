from django.contrib import admin
from talk.models import MessageLog
# Register your models here.


@admin.register(MessageLog)
class MessageLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'fromuser', 'touser', 'content', 'create_time', 'is_send']
    ordering = ('id',)
