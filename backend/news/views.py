from django.shortcuts import render
from rest_framework.views import APIView
from news.models import News
from news.serializers import EachNewsSerializer
from django.http import JsonResponse
from user.models import UserToken
import datetime


def recommand_like(age, like_list):
    # 计算推荐内容
    pass


class GetLikeAPIView(APIView):
    '''
    获取喜欢的信息
    post:
    '''
    def post(self, request):
        ret = {'code': 200, 'detail': 'success', 'info': []}
        token = request.GET.get('token')
        user = UserToken.objects.get(token__exact=token).user
        # 喜欢类型
        likes = user.like
        like_list = likes.split(',')  # [1, 2, 3, 4, 5]
        for like in like_list:
            news = News.objects.filter(type__exact=like)
            ser = EachNewsSerializer(instance=news, many=True)
            for s in ser.data:
                ret['info'].append(s)

        # 计算年龄
        birth = user.birth
        age = int((datetime.date.today() - birth).days/365)
        print('age: ', age)

        return JsonResponse(ret)


# Create your views here.
class GetFruitAPIView(APIView):
    '''
    获取水果信息
    '''
    def post(self, request):
        ret = {'code': 200, 'detail': 'success', 'info': []}
        news = News.objects.filter(type__exact=5)
        ser = EachNewsSerializer(instance=news, many=True)
        ret['info'] = ser.data
        return JsonResponse(ret)


class GetHotpotAPIView(APIView):
    '''
    获取火锅信息
    '''
    def post(self, request):
        ret = {'code': 200, 'detail': 'success', 'info': []}
        news = News.objects.filter(type__exact=6)
        ser = EachNewsSerializer(instance=news, many=True)
        ret['info'] = ser.data
        return JsonResponse(ret)


class GetMilkteaAPIView(APIView):
    '''
    获取奶茶信息
    '''
    def post(self, request):
        ret = {'code': 200, 'detail': 'success', 'info': []}
        news = News.objects.filter(type__exact=7)
        ser = EachNewsSerializer(instance=news, many=True)
        ret['info'] = ser.data
        return JsonResponse(ret)


class GetMealAPIView(APIView):
    '''
    获取三餐信息
    '''
    def post(self, request):
        ret = {'code': 200, 'detail': 'success', 'info': []}
        news = News.objects.filter(type__exact=8)
        ser = EachNewsSerializer(instance=news, many=True)
        ret['info'] = ser.data
        return JsonResponse(ret)


class GetBallAPIView(APIView):
    '''
    获取球类信息
    '''
    def post(self, request):
        ret = {'code': 200, 'detail': 'success', 'info': []}
        news = News.objects.filter(type__exact=9)
        ser = EachNewsSerializer(instance=news, many=True)
        ret['info'] = ser.data
        return JsonResponse(ret)


class GetRunAPIView(APIView):
    '''
    获取跑步信息
    '''
    def post(self, request):
        ret = {'code': 200, 'detail': 'success', 'info': []}
        news = News.objects.filter(type__exact=10)
        ser = EachNewsSerializer(instance=news, many=True)
        ret['info'] = ser.data
        return JsonResponse(ret)


class GetSwimAPIView(APIView):
    '''
    获取游泳信息
    '''
    def post(self, request):
        ret = {'code': 200, 'detail': 'success', 'info': []}
        news = News.objects.filter(type__exact=11)
        ser = EachNewsSerializer(instance=news, many=True)
        ret['info'] = ser.data
        return JsonResponse(ret)


class GetYogaAPIView(APIView):
    '''
    获取瑜伽信息
    '''
    def post(self, request):
        ret = {'code': 200, 'detail': 'success', 'info': []}
        news = News.objects.filter(type__exact=12)
        ser = EachNewsSerializer(instance=news, many=True)
        ret['info'] = ser.data
        return JsonResponse(ret)


class GetEnglishAPIView(APIView):
    '''
    获取英语信息
    '''
    def post(self, request):
        ret = {'code': 200, 'detail': 'success', 'info': []}
        news = News.objects.filter(type__exact=13)
        ser = EachNewsSerializer(instance=news, many=True)
        ret['info'] = ser.data
        return JsonResponse(ret)


class GetHandwritingAPIView(APIView):
    '''
    获取书法信息
    '''
    def post(self, request):
        ret = {'code': 200, 'detail': 'success', 'info': []}
        news = News.objects.filter(type__exact=14)
        ser = EachNewsSerializer(instance=news, many=True)
        ret['info'] = ser.data
        return JsonResponse(ret)


class GetDrawAPIView(APIView):
    '''
    获取绘画信息
    '''
    def post(self, request):
        ret = {'code': 200, 'detail': 'success', 'info': []}
        news = News.objects.filter(type__exact=15)
        ser = EachNewsSerializer(instance=news, many=True)
        ret['info'] = ser.data
        return JsonResponse(ret)


class GetReadAPIView(APIView):
    '''
    获取读书信息
    '''
    def post(self, request):
        ret = {'code': 200, 'detail': 'success', 'info': []}
        news = News.objects.filter(type__exact=16)
        ser = EachNewsSerializer(instance=news, many=True)
        ret['info'] = ser.data
        return JsonResponse(ret)


class GetSingAPIView(APIView):
    '''
    获取唱K信息
    '''
    def post(self, request):
        ret = {'code': 200, 'detail': 'success', 'info': []}
        news = News.objects.filter(type__exact=17)
        ser = EachNewsSerializer(instance=news, many=True)
        ret['info'] = ser.data
        return JsonResponse(ret)


class GetFilmAPIView(APIView):
    '''
    获取电影信息
    '''
    def post(self, request):
        ret = {'code': 200, 'detail': 'success', 'info': []}
        news = News.objects.filter(type__exact=18)
        ser = EachNewsSerializer(instance=news, many=True)
        ret['info'] = ser.data
        return JsonResponse(ret)


class GetChessAPIView(APIView):
    '''
    获取下棋信息
    '''
    def post(self, request):
        ret = {'code': 200, 'detail': 'success', 'info': []}
        news = News.objects.filter(type__exact=19)
        ser = EachNewsSerializer(instance=news, many=True)
        ret['info'] = ser.data
        return JsonResponse(ret)


class GetHomepartyAPIView(APIView):
    '''
    获取轰趴信息
    '''
    def post(self, request):
        ret = {'code': 200, 'detail': 'success', 'info': []}
        news = News.objects.filter(type__exact=20)
        ser = EachNewsSerializer(instance=news, many=True)
        ret['info'] = ser.data
        return JsonResponse(ret)

