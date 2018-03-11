from django.db import models

# Create your models here.
class User (models.Model):
    username = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=50)
    userID = models.AutoField(primary_key=True)
    nickname = models.CharField(max_length=50)
    listroot = models.IntegerField(null=True)
    birthday = models.DateField(null=True)
    email = models.EmailField()
    phonenum = models.CharField(max_length=20,null=True)
    image = models.ImageField(upload_to='img',null=True)



