from qiniu import Auth, put_file, etag
import qiniu.config
import time

class qiniu_pic(object):
    '''
    处理图片
    '''
    access_key = 'Ik5QrVDGrx-p-vYz4vVszKyqp6ZJHlXn6iEpGFtI'
    secret_key = 'zm5GITsidV6DD-hn-sg2T8G6BiQi1rPiBs6YItH4'

    def upload_pic(self, filename):
        # 构建鉴权对象
        q = Auth(self.access_key, self.secret_key)

        # 要上传的空间
        bucket_name = 'mybucket'

        # 要上传文件的本地路径
        localfile = '/home/me/Pictures/1.png'

        # 上传后保存的文件名
        filename = localfile.split('/')[-1]
        t = time.time()
        key = filename + str(round(t))

        # 生成上传Token,可以指定过期时间
        token = q.upload_token(bucket_name, key, 300)

        ret, info = put_file(token, key, localfile)
        # print('ret', ret)
        # print('info', info)

        return ret['key']  # 上传后保存的文件名

