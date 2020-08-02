# coding: utf-8
from django.shortcuts import render,redirect,HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from eggs import settings
from .models import EggSpot
from . import SpotNum,ResizePic
import hashlib
import time


def index(request):
    return render(request,'index.html')


def upload(request):
    return render(request,'pic-upload.html')


def success(request):
    return render(request,'upload-success.html')


def fail(request):
    return render(request,'upload-fail.html')


def make_file_id():  # 生成md5唯一id
    src = 'file'+str(time.time())
    m1 = hashlib.md5()
    m1.update(src.encode('utf8'))
    return m1.hexdigest()


# 上传并对图片进行压缩，识别处理
def upload_handle(request):
    try:
        src_path = settings.MEDIA_ROOT+'src/'
        dst_path = settings.MEDIA_ROOT+'dst/'
        resize_src_path = settings.MEDIA_ROOT+'resize/src/'
        resize_dst_path = settings.MEDIA_ROOT+'resize/dst/'
        base_url = 'http:127.0.0.1:8888/'
        pic = request.FILES['pic']
        if pic:
            pic_id = make_file_id()
            context = {
                'pic_id': pic_id
            }
            pic_name = '%s.%s'%(pic_id,pic.name.split('.')[1])
            # print(pic_name)
            save_path = '%ssrc/%s'%(settings.MEDIA_ROOT,pic_name)
            with open(save_path,'wb') as f:
                # 3 获取上传的文件内容并写入到服务器的保存路径中
                for content in pic.chunks():
                    f.write(content)
            url = base_url+'src/'+pic_id+'.'+pic.name.split('.')[1]
            dst_url = base_url+'dst/'+pic_id+'.'+pic.name.split('.')[1]
            # 进行识别处理
            spot_num,spot_square=SpotNum.deal_spot_pic(save_path,dst_path+pic_name)
            # 对图片进行压缩
            ResizePic.resize(save_path,resize_src_path+pic_name)
            ResizePic.resize(dst_path+pic_name,resize_dst_path+pic_name)
            if spot_num>0:
                is_dark_spots = 1
            else:
                is_dark_spots = 0
            EggSpot.objects.create(picture_id=pic_id, path=url,spot_num=spot_num,spot_square=spot_square,is_dark_spots=is_dark_spots,dst_url=dst_url)
            return redirect('/upload_success',context)
    except Exception as e:
        print("error:  ",e)
        return redirect('/upload_fail')


def details(request):
    eggSpots = EggSpot.objects.all()
    paginator = Paginator(eggSpots, 10)
    page = request.GET.get("page", 1)
    currentPage = int(page)
    context = {
        'eggSpots':eggSpots
    }

    try:
        eggSpots = paginator.page(page)
    except PageNotAnInteger:
        eggSpots=paginator.page(1)
    except EmptyPage:
        eggSpots=paginator.page(paginator.num_pages)
    return render(request,'pic-infos.html',locals())


def data(request):
    nid = request.GET.get('pic_id')
    # print(nid)
    pic_detail = EggSpot.objects.get(picture_id=nid)
    pic_id = pic_detail.picture_id
    src_url = pic_detail.path
    dst_url = pic_detail.dst_url
    spot_num = pic_detail.spot_num
    spot_square = pic_detail.spot_square
    context ={
        'pic_id':pic_id,
        'src_url':src_url,
        'dst_url':dst_url,
        'spot_num':spot_num,
        'spot_square':spot_square,
        'pic_detail':pic_detail
    }
    return render(request,'pic-details.html',context)



# https://blog.csdn.net/cxh6863/article/details/88381235  图片url



