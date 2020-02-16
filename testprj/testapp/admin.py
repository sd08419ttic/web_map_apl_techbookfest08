#from django.contrib import admin
from django.contrib.gis import admin    #地図モジュール用のadminに変更

# Register your models here.
from testapp.models import Station_MODEL                 #modelsに記述したクラス名に合わせる
from testapp.models import Public_Facility_MODEL         #modelsに記述したクラス名に合わせる
from testapp.models import Station_Info_MODEL            #modelsに記述したクラス名に合わせる
from testapp.models import RailRoadSection_info_MODEL    #modelsに記述したクラス名に合わせる

admin.site.register(Station_MODEL)                       #2章　データの編集・管理画面(Admin)
admin.site.register(Public_Facility_MODEL,admin.OSMGeoAdmin)         #OpenStreetMapで表示するように設定
admin.site.register(Station_Info_MODEL,admin.OSMGeoAdmin)            #OpenStreetMapで表示するように設定
admin.site.register(RailRoadSection_info_MODEL,admin.OSMGeoAdmin)    #OpenStreetMapで表示するように設定