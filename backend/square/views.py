from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from square.models import Square
from user.models import UserToken
from square.serializers import SquareSerializer


# Create your views here.
# 完
class GetAllSquareAPIView(APIView):
    '''
    获取全部广场信息
    '''
    def post(self, request):
        ret = {'code': 200, 'detail': 'success', 'info': []}
        square = Square.objects.all()
        ser = SquareSerializer(instance=square, many=True)
        ret['info'] = ser.data
        return JsonResponse(ret)


# 完
class AddSquareAPIView(APIView):
    '''
    增加广场信息
    '''
    def post(self, request):
        ret = {'code': 200, 'detail': 'success'}
        token = request.GET.get('token')
        content = request.data.get('content')

        s = Square()
        s.user = UserToken.objects.filter(token__exact=token)[0].user
        s.content = content
        s.save()
        return JsonResponse(ret)
