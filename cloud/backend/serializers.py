from django.contrib.auth.models import User as AdminUser,Group
from rest_framework import serializers
from backend.models import User


class AdminUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AdminUser
        fields = ('url', 'username', 'email', 'groups')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'userID', 'nickname', 'listroot', 'birthday','email', 'phonenum','image')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')