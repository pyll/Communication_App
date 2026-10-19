from django.contrib import admin
from friend.models import *
# Register your models here.


@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    list_display = ['id', 'user1', 'user2', 'is_deleted']
    ordering = ('id',)


@admin.register(FriendLog)
class FriendLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'user1', 'user2', 'is_agreed']
    ordering = ('id',)
