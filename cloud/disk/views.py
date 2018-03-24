from django.shortcuts import render
from django.http import JsonResponse,HttpResponse,StreamingHttpResponse
from backend.models import User
from io import StringIO
from .models import Folder
from .models import File
import urllib.parse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone as datetime
import os
import hashlib
from .hdfs import WebHdfs
from cloud.settings import HADOOP_HOST,HADOOP_PORT,HADOOP_USERNAME,MEDIA_ROOT
# Create your views here.
def count(num) :
    ans = str(num)+"B";
    if num >= 1024 :
        ans = str(num//1024) + "K"
        num = num/1024
    if num >= 1024 :
        ans = str(num//1024) + "M"
        num = num/1024
    if num >= 1024 :
        ans = str(num//1024) + "G"
        num = num/1024
    return ans
@csrf_exempt
def list(request) :
    if request.method == 'POST' :
        post = json.loads(request.body.decode('utf-8'))
        userID = post.get('userID')
        nowid = post.get('nowid')
        print('from list nowid:'+str(nowid))
        list = []
        listid = []
        size = []
        update = []
        qlist = File.objects.filter(userid=userID, fatherid=nowid)
        for e in qlist:
            list.append(e.foldername)
            listid.append(e.id)
            size.append(e.size)
            update.append(e.update)
        le = len(list)
        qlist = Folder.objects.filter(userid=userID, fatherid=nowid)
        ok = False
        for e in qlist:
            ok = False
            for i in range(le):
                if(listid[i]==e.id) :
                    ok = True
                    break
            if ok == False:
                list.append(e.foldername)
                listid.append(e.id)
                size.append(-1)
                update.append(e.update)
        cSize = []
        for s in size:
            if s == -1:
                cSize.append(-1);
            else :
                cSize.append(count(s));
        return JsonResponse({'data':'ok' ,'list': list,
                             'listid': listid, 'size': cSize,'update':update})


@csrf_exempt
def newfolder (request):
    if request.method == 'POST' :
        post = json.loads(request.body.decode('utf-8'))
        userid = post.get('userID')
        nowid = post.get('nowid')
        print(nowid)
        foldername = post.get('foldername')
        folder = Folder(userid = int(userid),foldername = foldername,fatherid = nowid,
                        update = datetime.now() )
        folder.save()
        return JsonResponse({'data':'ok' ,'listid': folder.id,
                             'update':datetime.now()})


@csrf_exempt
def enterfolder (request) :
    if request.method == 'POST':
        post = json.loads(request.body.decode('utf-8'))
        userid = post.get('userID')
        nowid = post.get('nowid')
        qlist = Folder.objects.filter(userid=userid, fatherid=nowid)
        list = []
        listid = []
        size = []
        update = []
        for e in qlist:
            list.append(e.foldername)
            listid.append(e.id)
            size.append(0)
            update.append(e.update)
        qlist = File.objects.filter(userid=userid, fatherid=nowid)
        for e in qlist:
            list.append(e.foldername)
            listid.append(e.id)
            size.append(e.size)
            update.append(e.update)
        return JsonResponse({'data': 'ok', 'list': list,
                             'listid': listid, 'size': size, 'update': update})


def get_FileSize(fsize):
    fsize = fsize/float(1024*1024)
    return round(fsize,2)


def download(request) :
    if request.method == 'GET':
        fileid=request.GET.get('fileid')
        filename = request.GET.get('filename')
        findfile = File.objects.filter(id=fileid)
        md5 = findfile[0].md5
        webclient = WebHdfs(HADOOP_HOST, HADOOP_PORT, HADOOP_USERNAME)
        file = webclient.download('/'+md5)
        if(file['status']=='ok'):
            response = StreamingHttpResponse(file['file'])
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="{0}"'.format(filename)
            return response
        else:
            return HttpResponse("505")
    return HttpResponse("404")

@csrf_exempt
def upload(request) :
    if request.method == "POST":
        post=request.POST
        userid = post.get('userID')
        nowid = post.get('nowid')
        upfile = request.FILES.get('file')
        hash_md5 = hashlib.md5()
        print('yes?')
        f=None
        for chunk in iter(lambda: upfile.read(4096), b""):
            hash_md5.update(chunk)#累加
            if f==None:
                f=chunk
            else:
                f=f+chunk
        hash = hash_md5.hexdigest()
        webclient = WebHdfs(HADOOP_HOST,HADOOP_PORT,HADOOP_USERNAME)
        target_path = '/'+hash
        findhash  = File.objects.filter(md5=hash)
        if findhash.exists() :
            pass
        else :
            webclient.copyFromLocal(f, target_path)
        file = File(userid=userid,foldername=upfile.name,fatherid=nowid,update=datetime.now(),
                    size=upfile.size,md5=hash)
        file.save()

        return JsonResponse({'data':'ok'})
