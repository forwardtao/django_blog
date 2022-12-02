import os 
import uuid
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings


# @csrf_exempt
# def upload_file(request):
#     # 获取表单上传的图片
#     upload = request.FILES.get('upload')

#     uid = ''.join(str(uuid.uuid4()).split('-'))
#     print(uid)
#     # 修改图片名称
#     names = str(upload.name).split('.')
#     names[0] = uid
#     # 返回修改过的图片名称
#     upload.name = ''.join(names)
#     print(upload.name)
#     new_path = os.path.join(settings.MEDIA_ROOT,'upload/',upload.name)
#     with open(new_path,'wb+') as f:
#         for chunk in upload.chunks():
#             f.write(chunk)
    
#     filename  =  upload.name
#     url = '/media/upload/' + filename
#     retdata = {
#         'url':url,
#         'upload':'1',
#         'fileName':filename,
#     }
#     return JsonResponse(retdata)


@csrf_exempt
def upload_file(request):

    # 获取表单上传的图片
    upload = request.FILES.get('upload')
    # 返回uid
    uid = ''.join(str(uuid.uuid4()).split('-'))
    # 修改图片名称
    # asdasd.jpg  fddg.png  ['sasda', 'jpg']
    names = str(upload.name).split('.')
    names[0] = uid
    # 返回修改过的图片格式
    upload.name = '.'.join(names)
    
    new_path = os.path.join(settings.MEDIA_ROOT, 'upload/', upload.name) 
    # 上传图片
    with open(new_path, 'wb+') as file:
        for chunk in upload.chunks():
            file.write(chunk)
    
    # 构造要求的数据格式并返回
    filename = upload.name
    url = '/media/upload/' + filename
    retdata = { 'url': url,         #上传图片完整url
                'uploaded': '1',   # 上传成功标识
                'fileName': filename }   # 上传图片名称
    return JsonResponse(retdata)