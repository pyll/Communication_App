from rest_framework.views import APIView
from django.http import JsonResponse
from event.serializers import *
from user.models import UserToken
from rest_framework.views import APIView


# Create your views here.
# 完
class GetAllEventAPIView(APIView):
    '''
    获取所有动态
    '''
    def post(self, request):
        ret = {'code': 200, 'detail': 'success', 'info': []}
        events = Event.objects.all()
        ser = EventSerializer(instance=events, many=True)
        ret['info'] = ser.data
        return JsonResponse(ret)


# 完
class GetFoodEventAPIView(APIView):
    '''
    获取食类型动态
    '''
    def post(self, request):
        ret = {'code': 200, 'detail': 'success', 'info': []}
        foodEvents = Event.objects.filter(type=1)
        for e in foodEvents:
            if e.is_deleted == 1:
                continue
            ser = EachEventSerializer(instance=e)
            ret['info'].append(ser.data)
        return JsonResponse(ret)


# 完
class GetSportEventAPIView(APIView):
    '''
    获取运动类型动态
    '''
    def post(self, request):
        ret = {'code': 200, 'detail': 'success', 'info': []}
        sportEvents = Event.objects.filter(type=2)
        for e in sportEvents:
            if e.is_deleted == 1:
                continue
            ser = EachEventSerializer(instance=e)
            ret['info'].append(ser.data)
        return JsonResponse(ret)


# 完
class GetStudyEventAPIView(APIView):
    '''
    获取学习类型动态
    '''
    def post(self, request):
        ret = {'code': 200, 'detail': 'success', 'info': []}
        studyEvents = Event.objects.filter(type=3)
        for e in studyEvents:
            if e.is_deleted == 1:
                continue
            ser = EachEventSerializer(instance=e)
            ret['info'].append(ser.data)
        return JsonResponse(ret)


# 完
class GetPlayEventAPIView(APIView):
    '''
    获取娱乐类型动态
    '''
    def post(self, request):
        ret = {'code': 200, 'detail': 'success', 'info': []}
        playEvents = Event.objects.filter(type=4)
        for e in playEvents:
            if e.is_deleted == 1:
                continue
            ser = EachEventSerializer(instance=e)
            ret['info'].append(ser.data)
        return JsonResponse(ret)


# 完
class GetMyEventAPIView(APIView):
    '''
    获取我的动态
    '''
    def post(self, request):
        ret = {'code': 200, 'detail': 'success', 'info': []}
        token = request.GET.get('token')
        u_id = UserToken.objects.get(token__exact=token).user_id
        myEvents = Event.objects.filter(user_id__exact=u_id)
        for e in myEvents:
            if e.is_deleted == 1:
                continue
            ser = EventSerializer(instance=e)
            ret['info'].append(ser.data)
        return JsonResponse(ret)


# 完
class DelMyEventAPIView(APIView):
    '''
    删除我的动态
    '''
    def post(self, request):
        ret = {'code': 200, 'detail': 'success'}
        id = request.data.get('id')
        e = Event.objects.get(id__exact=id)
        e.is_deleted = 1
        e.save()
        return JsonResponse(ret)


# 完
class AddEventAPIView(APIView):
    # 用户发布动态
    def post(self, request):
        ret = {'code': 200, 'detail': 'success'}
        token = request.GET.get('token')
        # data = request.data
        content = request.data.get('content')
        type = request.data.get('type')

        e = Event()
        e.type = EventType.objects.filter(type__exact=type)[0]
        e.user = UserToken.objects.filter(token__exact=token)[0].user
        e.content = content
        e.save()
        return JsonResponse(ret)

