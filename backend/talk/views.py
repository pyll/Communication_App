import threading
from dwebsocket.decorators import accept_websocket
from talk.models import MessageLog
import json
from datetime import datetime

# 存储连接websocket的用户
clients = {}
# 记录房间数   其实没什么卵用  = =
count = 0


def hasUnSend(user1, user2, user1_socket):
    # 检查有未接收的消息
    logs = MessageLog.objects.filter(fromuser=user2, touser=user1, is_send=0)
    for log in logs:
        time = log.create_time.strftime('%Y-%m-%d %H:%M:%S')
        msg = {'from_user': user2, 'to_user': user1, 'time': time, 'content': log.content}
        print('unsend msg: ', msg)
        b1 = json.dumps(msg).encode('utf-8')
        user1_socket.send(b1)
        log.is_send = 1
        log.save()


def saveDatabase(message, send):
    # 保存到数据库
    messagelog = MessageLog()
    messagelog.fromuser = message['from_user']
    messagelog.touser = message['to_user']
    messagelog.content = message['content']
    messagelog.create_time = message['time']
    messagelog.is_send = send
    messagelog.save()


# 连接websocket  ws://localhost：8000/talk/websocketLink/roomname
# 因为 websocket 是协议  所以不能用 http或https
@accept_websocket
def websocketLink(request, roomname):
    '连接websocket'
    global count
    # 获取连接
    if request.is_websocket:
        lock = threading.RLock()  # rlock线程锁
        try:
            lock.acquire()  # 抢占资源
            s = {}
            user2_user1 = roomname.split('_')[1] + '_' + roomname.split('_')[0]
            #  因为同一个账号打开多个页面连接信息是不同的
            if clients.get(user2_user1) != None:
                roomname = user2_user1
            if clients.get(roomname) != None:  # 房间名已存在,第二位用户连入
                # 房间存在, 判断连入用户名
                username = ''
                flag = 1
                for client in clients[roomname]:
                    if clients[roomname][client]['username'] == roomname.split('_')[1]:
                        username = roomname.split('_')[0]  # user1
                    else:
                        username = roomname.split('_')[1]  # user2
                        flag = 0
                # 连接信息  键 连接名  值：连接保存
                s[str(request.websocket)] = {}
                s[str(request.websocket)]['socket'] = request.websocket
                s[str(request.websocket)]['username'] = username
                # 已存在的连接信息继续增加
                clients[roomname].update(s)
                hasUnSend(username, roomname.split('_')[flag], request.websocket)  # 发送未发消息
            else:  # 房间名未存在,第一位用户连入
                # 人数加1
                count = count + 1
                # 发起聊天的用户名
                username = roomname.split('_')[0]  # user1
                #  连接信息  键 连接名  值：连接保存
                s[str(request.websocket)] = {}
                s[str(request.websocket)]['socket'] = request.websocket
                s[str(request.websocket)]['username'] = username
                # 新增 用户  连接信息
                clients[roomname] = s
                hasUnSend(username, roomname.split('_')[1], request.websocket)  # 发送未发消息
            print("用户人数" + str(count))
            print('roomname: ', roomname)
            print('clients[roomname]: ', clients[roomname])

            # 监听接收客户端发送的消息 或者 客户端断开连接
            for message in request.websocket:
                if not message:
                    print('no message')
                    break
                else:
                    # eg{'room_name': lily_rose, 'from_user': lily, 'to_user': rose, 'content': this.sendmessage}
                    message = json.loads(message.decode('utf-8'))
                    # 加上后台时间
                    message['time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print('============')
                    print('message: ', message)
                    message.pop('roomname')

                    websocketMsg(clients[roomname], message)
        finally:
            # 通过用户名找到 连接信息 再通过 连接信息 k 找到 v (k就是连接信息)
            clients.get(roomname).pop(str(request.websocket))
            if clients[roomname] == {}:  # 房间无人, 清理房间
                print('client[rooname] is empty')
                clients.pop(roomname)
            print('----------release-------------')
            print('clients: ', clients)
            # 释放锁
            lock.release()


# 发送消息
def websocketMsg(client, msg):
    # 房间中只有一个人, 目前假设只是发消息的人
    if len(client) == 1:
        for cli in client:
            # 保存入数据库, 消息未发送
            saveDatabase(msg, 0)
            # 只发给自己
            msg['to_user'] = client[cli]['username']
            b1 = json.dumps(msg).encode('utf-8')
            client[cli]['socket'].send(b1)

    # 遍历房间中的人
    else:
        for cli in client:
            print('cli: ', client)
            'client客户端 ，msg消息'
            # 自己给自己的消息
            if client[cli]['username'] == msg['from_user']:
                msg['to_user'] = client[cli]['username']
                print('msg: ', msg)
            else:  # 给对方发消息
                msg['to_user'] = client[cli]['username']
                saveDatabase(msg, 1)  # 保存数据库
            b1 = json.dumps(msg).encode('utf-8')
            client[cli]['socket'].send(b1)


# def websocketMsg(client, msg, roomname):
#     # 因为一个账号会有多个页面打开 所以连接信息需要遍历
#     # 只有一个人在房间
#     if len(client) == 1:
#         # 只发给自己, 存入数据库标记为未发
#         for cli in client:
#             # user1在
#             if roomname.split('_')[0] == msg['from_user']:
#                 # 存入数据库
#                 log = MessageLog()
#                 log.fromuser = msg['from_user']
#                 log.touser = msg['to_user']
#                 log.content = msg['content']
#                 log.create_time = datetime.now()
#                 log.is_send = 0  # 未发
#                 log.save()
#
#                 # 只发给自己
#                 msg['to_user'] = client[cli]['username']
#                 print('msg: ', msg)
#                 b1 = json.dumps(msg).encode('utf-8')
#                 client[cli]['socket'].send(b1)
#     else:
#         for cli in client:
#             print('cli: ', client)
#             'client客户端 ，msg消息'
#             # 自己给自己的消息
#             if client[cli]['username'] == msg['from_user']:
#                 msg['to_user'] = client[cli]['username']
#                 print('msg: ', msg)
#             else:
#                 msg['to_user'] = client[cli]['username']
#                 print('msg', msg)
#             b1 = json.dumps(msg).encode('utf-8')
#             client[cli]['socket'].send(b1)

