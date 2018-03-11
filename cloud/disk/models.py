from django.db import models

# Create your models here.
class Folder(models.Model) :
    id = models.AutoField(primary_key=True)
    userid = models.IntegerField()
    foldername = models.CharField(max_length=100)
    fatherid = models.IntegerField()
    update = models.DateTimeField()


class File(Folder):
    size = models.IntegerField(default=0)
    md5 = models.CharField(max_length=1000)