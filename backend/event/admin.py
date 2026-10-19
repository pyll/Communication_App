from django.contrib import admin
from event.models import *


# Register your models here.
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'content', 'type', 'send_time', 'is_deleted']
    ordering = ('id',)


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'tid']
    ordering = ('id',)
    empty_value_display = '无'


admin.site.site_header = '社交软件'
admin.site.site_title = '社交软件'
