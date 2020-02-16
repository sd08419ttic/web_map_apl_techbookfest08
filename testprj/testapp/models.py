#from django.db import models
from django.contrib.gis.db import models
# Create your models here.

#2章　データベースの管理 データベース構造の定義(models)
class Station_MODEL(models.Model):
    dataid = models.IntegerField("id")
    name = models.CharField("name",max_length=1024) #文字長さを制限
    latitude = models.FloatField("latitude")
    longitude = models.FloatField("longitude")

    def __str__(self):
        return self.name


class Public_Facility_MODEL(models.Model):
    p27_001 = models.CharField(u'行政区域コード',max_length=10)
    p27_002 = models.CharField(u'公共施設大分類',max_length=10)
    p27_003 = models.CharField(u'公共施設小分類',max_length=10)
    p27_004 = models.CharField(u'文化施設分類',max_length=10)
    p27_005 = models.CharField(u'名称',max_length=254)
    p27_006 = models.CharField(u'所在地',max_length=254)
    p27_007 = models.IntegerField(u'管理者コード',)
    p27_008 = models.IntegerField(u'階数',)
    p27_009 = models.IntegerField(u'建築年',)
    geom = models.PointField(srid=6668)

    def __str__(self):
        #運営会社_路線名
        return self.p27_005 + "_" + self.p27_006

class Station_Info_MODEL(models.Model):
    n02_001 = models.CharField(u'鉄道区分',max_length=1024)
    n02_002 = models.CharField(u'事業者種別',max_length=1024)
    n02_003 = models.CharField(u'路線名',max_length=1024)
    n02_004 = models.CharField(u'運営会社',max_length=1024)
    n02_005 = models.CharField(u'駅名',max_length=1024)
    geom = models.LineStringField(srid=6668)    #駅情報

    def __str__(self):
        #データ全体の名前 (admin画面用)
        return self.n02_005 + "_" + self.n02_003

class RailRoadSection_info_MODEL(models.Model):
    n02_001 = models.CharField(u'鉄道区分',max_length=1024)
    n02_002 = models.CharField(u'事業者種別',max_length=1024)
    n02_003 = models.CharField(u'路線名',max_length=1024)
    n02_004 = models.CharField(u'運営会社',max_length=1024)
    geom = models.LineStringField(srid=6668)    #路線情報

    def __str__(self):
    #データ全体の名前 (admin画面用)
        return self.n02_003 + "_" + self.n02_004
