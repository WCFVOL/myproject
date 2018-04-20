from django.shortcuts import render
from django.http import JsonResponse
from .models import User
from disk.models import Folder
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone as datetime
from django.contrib.auth.models import User as AdminUser, Group
from rest_framework import viewsets
from backend.serializers import AdminUserSerializer, GroupSerializer, UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AdminUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = AdminUser.objects.all().order_by('-date_joined')
    serializer_class = AdminUserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

@csrf_exempt
def register(request) :
    if request.method == "POST":
        post=request.POST
        username = post.get('username')
        password = post.get('password')
        image = request.FILES.get('image')
        testusername = User.objects.filter(username=username)
        if(testusername.exists()) :
            return JsonResponse({'data': '用户名已存在!'})
        email = post.get('email')
        user = User(username=username, password=password,email=email,image=image)
        user.save()
        folder = Folder(userid = user.userID,foldername = '全部文件',fatherid = 0,
                        update = datetime.now())
        folder.save()
        user.listroot = folder.id
        user.nickname = str(user.userID)
        user.save()
        return JsonResponse({'data': 'ok'})
    return JsonResponse({'data': '请求错误'})


@csrf_exempt
def login(request) :
    if request.method == "POST":
       #print("---------+++++++++++++++++++-----")
        post=json.loads(request.body.decode('utf-8'))
        username = post.get('username')
        password = post.get('password')
        user = User.objects.filter(username=username)[0]
        if(user.password==password):
            return JsonResponse({'data': 'ok','username': str(user.username),'nickname':
                                 str(user.nickname),'image': str(user.image),'email':str(user.email),'userID':str(user.userID)})
    return JsonResponse({'data': 'no'})
