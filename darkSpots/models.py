from django.db import models

# Create your models here.


class EggSpot(models.Model):   #一个类对应一个表
    picture_id = models.CharField(max_length=50)
    path = models.CharField(max_length=255)
    is_dark_spots = models.SmallIntegerField()
    spot_num = models.IntegerField()
    spot_square = models.FloatField(max_length=255)
    dst_url = models.CharField(max_length=255)




