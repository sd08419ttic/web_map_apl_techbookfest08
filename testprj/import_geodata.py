#!/usr/bin/env python
#import
import os
import django
#5章　国土地理院地図DBインポート
#下記行はmanage.pyからコピーする (プロジェクト名によって異なる)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testprj.settings')
django.setup()

from django.contrib.gis.utils import LayerMapping
from testapp.models import Public_Facility_MODEL,Station_Info_MODEL,RailRoadSection_info_MODEL 

# ModelとDBファイルのカラム名のマッピングを行う
mapping_Public_Facility = {
    'p27_001' : 'P27_001',
    'p27_002' : 'P27_002',
    'p27_003' : 'P27_003',
    'p27_004' : 'P27_004',
    'p27_005' : 'P27_005',
    'p27_006' : 'P27_006',
    'p27_007' : 'P27_007',
    'p27_008' : 'P27_008',
    'p27_009' : 'P27_009',
    'geom'    : 'POINT',
}

mapping_Station_Info = {
    'n02_001' : 'N02_001',
    'n02_002' : 'N02_002',
    'n02_003' : 'N02_003',
    'n02_004' : 'N02_004',
    'n02_005' : 'N02_005',
    'geom'    : 'LineString',
}

mapping_RailRoadSection_info = {
    'n02_001' : 'N02_001',
    'n02_002' : 'N02_002',
    'n02_003' : 'N02_003',
    'n02_004' : 'N02_004',
    'geom'    : 'LineString',
}

# ファイルパス
public_facility_file_path = 'data/'+'P27-13_13.shp'
station_info_file_path = 'data/'+'N02-18_Station.geojson'
railroadsection_info_file_path = 'data/'+'N02-18_RailroadSection.geojson'

def read_Public_Facility():
    lm = LayerMapping(Public_Facility_MODEL, public_facility_file_path, mapping_Public_Facility, transform=False, encoding='UTF-8')
    lm.save(strict=True)

def read_Station_Info():
    lm = LayerMapping(Station_Info_MODEL, station_info_file_path, mapping_Station_Info, transform=False, encoding='UTF-8')
    lm.save(strict=True)

def read_RailRoadSection_info():
    lm = LayerMapping(RailRoadSection_info_MODEL, railroadsection_info_file_path, mapping_RailRoadSection_info, transform=False, encoding='UTF-8')
    lm.save(strict=True)

if __name__ == '__main__':
    Public_Facility_MODEL.objects.all().delete()
    print("Start_Importing_File")
    read_Public_Facility()
    read_Station_Info()
    read_RailRoadSection_info()
    print("Finished!")