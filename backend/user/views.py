from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password, check_password
import time
import hashlib
from user.models import User, UserToken
from friend.models import Friend, FriendLog
from django.http import JsonResponse
from user.serializers import RegisterSerializer, UserSerializer, FriendSerializer
from qiniu import Auth, put_file
from user.utils.config import configs
from django.db.models import Q


# 加密手机号+时间得到token
def md5(username):
    ctime = str(time.time())
    m = hashlib.md5(bytes(username, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()


def setAvatar(username, avatar):
    q = Auth(configs['qiniu']['access_key'], configs['qiniu']['secret_key'])
    bucket_name = 'privatebucket'  # 上传的空间
    key = username + '.png'  # 上传的文件名
    token = q.upload_token(bucket_name, key, 300)  # 生成上传Token,可以指定过期时间
    # img = avatar.save('/home/me/pic/' + username + '.png')
    # filename = '/home/me/pic/' + username + '.png'
    # with open(filename, 'wb') as f:
    #     f.write(avatar)
    filename = avatar
    ret, info = put_file(token, key, filename)
    bucket_domain = 'ppp1y73gt.bkt.clouddn.com'
    base_url = 'http://%s/%s' % (bucket_domain, ret['key'])
    private_url = q.private_download_url(base_url, expires=3600)
    # print('private_url: ', private_url)
    return private_url


class TestAPIView(APIView):
    '''
    测试接口
    '''
    authentication_classes = []

    def post(self, request):
        print(request.data)
        return JsonResponse({'detail': '我收到啦!!!!!!'})


# 假设图片流是二进制数据
class RegisterAPIView(APIView):
    # 注册
    authentication_classes = []

    def post(self, request):
        ret = {'code': 201, 'detail': {}}
        data = request.data
        flag = 0
        if User.objects.filter(username__exact=data['username']):
            flag = 1
            ret['detail']['username'] = '该用户名已被注册'
        if data['password'] != data['re_password']:
            flag = 1
            ret['detail']['password'] = '两次密码不一样'
        if flag == 1:
            return JsonResponse(ret)
        username = data.get('username')
        new_user = {
            'username': username,
            'password': make_password(data.get('password'), salt=username),
            'school': data.get('school'),
            'gender': data.get('gender'),
            'avatar': setAvatar(data.get('username'), data.get('avatar'))  # 前端传来的图片
        }
        ser = RegisterSerializer(data=new_user)
        if ser.is_valid(raise_exception=True):
            print(ser.validated_data)
            ser.save()
            ret['code'] = 200
            ret['detail'] = 'success'
        else:
            print(ser.errors)
            ret['detail'] = ser.errors
        return JsonResponse(ret)

# 完
class LoginAPIView(APIView):
    # 登录
    authentication_classes = []

    def post(self, request):
        ret = {'code': 201, 'detail': '未知错误', 'info': []}
        print(request.user)
        data = request.data
        username = data.get('username')
        password = data.get('password')
        # 检查手机号是否存在
        try:
            user = User.objects.get(username__exact=username)
        except User.DoesNotExist:
            user = None
        # 检查密码是否正确
        if user:
            if check_password(password, user.password):
                serializer = UserSerializer(user)
                token = md5(username)  # 加密
                UserToken.objects.update_or_create(user=user, defaults={'token': token})  # 创建token
                # print(new_data)
                new_obj = {
                    'username': serializer.data.get('username'),
                    'gender': serializer.data.get('gender'),
                    'school': serializer.data.get('school'),
                    'token': token,
                    'avatar': serializer.data.get('avatar'),
                    'birth': serializer.data.get('birth'),
                    'major': serializer.data.get('major'),
                }
                ret['code'] = 200
                ret['detail'] = 'success'
                ret['info'] = new_obj
                return JsonResponse(ret)
            else:
                ret['detail'] = '密码不正确'
                return JsonResponse(ret)
        else:
            ret['detail'] = '用户不存在'
            return JsonResponse(ret)


class UpdateAPIView(APIView):
    '''
    更新用户信息
    '''
    def post(self, request):
        ret = {'code': 200, 'detail': 'success'}
        token = request.GET.get('token')
        u = UserToken.objects.get(token__exact=token).user
        u.school = request.data.get('school')
        u.gender = request.data.get('gender')
        u.username = request.data.get('username')
        u.save()
        return JsonResponse(ret)


# 完
class GetFriendListAPIView(APIView):
    '''
    获取好友列表
    '''
    def post(self, request):
        ret = {'code': 200, 'detail': 'success', 'info': []}
        token = request.GET.get('token')
        u = UserToken.objects.get(token__exact=token).user
        friends = Friend.objects.filter(Q(user1__exact=u) | Q(user2__exact=u))
        for friend in friends:
            if friend.is_deleted == 1:  # 已删除好友
                continue
            f = None
            if friend.user1 == u:
                f = friend.user2
            elif friend.user2 == u:
                f = friend.user1
            f = User.objects.get(username__exact=f)
            ser = FriendSerializer(f)
            ret['info'].append(ser.data)
        return JsonResponse(ret)


# 未完, 不知道如何实时发给用户
class AddFriendAPIView(APIView):
    '''
    添加好友, 请求先存在friend_log中
    '''
    def post(self, request):
        ret = {'code': 200, 'detail': 'success'}
        token = request.GET.get('token')
        username = request.data.get('username')
        u = UserToken.objects.get(token__exact=token).user
        f = User.objects.get(username__exact=username)
        # 判断是否在Friend表中有此好友关系
        relation = FriendLog.objects.filter(Q(user1_id__exact=f, user2_id__exact=u) | Q(user1_id__exact=u, user2_id__exact=f))
        if relation:  # 已发送过请求
            relation[0].is_agreed = 0  # 更新好友请求关系
            relation[0].save()
            return JsonResponse(ret)
        addf = FriendLog()
        addf.user1 = u
        addf.user2 = f
        addf.save()
        return JsonResponse(ret)


# 完
class ResponseAddFriendAPIView(APIView):
    '''
    对好友请求的回复接口, 将friend_log的请求放到friend中
    '''
    def post(self, request):
        ret = {'code': 200, 'detail': 'success'}
        token = request.GET.get('token')
        username = request.data.get('username')
        u = UserToken.objects.get(token__exact=token).user
        f = User.objects.get(username__exact=username)
        # 判断是否在Friend表中有此好友关系
        relation = Friend.objects.filter(Q(user1_id__exact=f, user2_id__exact=u) | Q(user1_id__exact=u, user2_id__exact=f))
        if relation:  # 先前建立关系
            if relation[0].is_deleted == 1:  # 后来删除,现在要重新建立关系
                relation[0].is_deleted = 0
                relation[0].save()
                return JsonResponse(ret)
            else:  # 关系还存在
                ret['detail'] = '已建立此好友关系'
                return JsonResponse(ret)
        addf = Friend()
        addf.user1 = u
        addf.user2 = f
        addf.save()  # 增加到Friend
        # 修改FriendLog中的is_agreed值,为同意
        agree = FriendLog.objects.get(user2_id__exact=u)
        agree.is_agreed = 1
        agree.save()
        return JsonResponse(ret)


# 完
class DeleteFriendAPIView(APIView):
    '''
    删除好友
    '''
    def post(self, request):
        ret = {'code': 200, 'detail': 'success'}
        token = request.GET.get('token')
        fusername = request.data.get('username')
        # 用户id
        u_id = UserToken.objects.get(token__exact=token).user_id
        # 好友id
        f_id = User.objects.get(username__exact=fusername).id
        f = Friend.objects.get(Q(user1_id__exact=f_id, user2_id__exact=u_id) | Q(user1_id__exact=u_id, user2_id__exact=f_id))
        f.is_deleted = 1
        f.save()
        return JsonResponse(ret)


# 完
class GetUserInfoAPIView(APIView):
    '''
    获取用户信息
    '''
    def post(self, request):
        ret = {'code': 200, 'detail': 'success'}
        token = request.GET.get('token')
        u = UserToken.objects.get(token__exact=token).user
        ser = FriendSerializer(instance=u)
        ret['info'] = ser.data
        return JsonResponse(ret)


# 完
class SurveyAPIView(APIView):
    '''
    保存问卷内容
    '''
    def post(self, request):
        ret = {'code': 200, 'detail': 'success'}
        token = request.GET.get('token')
        user = UserToken.objects.get(token__exact=token).user
        user.birth = request.data.get('birth')
        user.major = request.data.get('major')
        user.event_type = request.data.get('like')
        user.save()
        return JsonResponse(ret)
