# -*- coding: utf-8 -*-
from django.urls import path
from django.conf.urls import url
from djgeojson.views import GeoJSONLayerView
from testapp.models import Station_MODEL                 #modelsに記述したクラス名に合わせる
from testapp.models import Public_Facility_MODEL         #modelsに記述したクラス名に合わせる
from testapp.models import Station_Info_MODEL            #modelsに記述したクラス名に合わせる
from testapp.models import RailRoadSection_info_MODEL    #modelsに記述したクラス名に合わせる
from . import views

urlpatterns = [
    path('', views.hello, name='hello'),                                        #2章 Django Hello World
    url(r'^template/$', views.hello_template, name='hello_template'),           #2章 Django Template (Templateを使ったWebページ実装)
    url(r'^template_3_1/$', views.html_structure, name='template_3_1'),         #3章 HTML 構造
    url(r'^template_3_2/$', views.html_text_p_h, name='template_3_2'),          #3章 HTML P/Hタグ
    url(r'^template_3_3/$', views.html_hyperlink, name='template_3_3'),         #3章 HTML ハイパーリンク
    url(r'^template_3_4/$', views.html_image, name='template_3_4'),             #3章 HTML 画像表示
    url(r'^template_3_5/$', views.css_basic, name='template_3_5'),              #3章 CSS (基本)
    url(r'^template_3_6/$', views.css_with_ID, name='template_3_6'),            #3章 CSS (ID指定)
    url(r'^template_3_7/$', views.css_with_Layout, name='template_3_7'),        #3章 CSS (レイアウト/フローティング)
    url(r'^template_3_8/$', views.html_webform, name='html_webform'),           #3章 フォーム (セレクトボックス・ラジオボタン・チェックボックス)
    url(r'^template_3_9/$', views.html_dbshowdata, name='template_3_9'),        #3章 データベースの表示
    url(r'^template_3_10/$', views.html_dbselectbox, name='db_selectbox'),      #3章 データベースをセレクトボックスに指定
    url(r'^template_3_11/$', views.db_test_update, name='db_update'),           #3章 データベースを更新

    url(r'^template_4_1/$', views.leaflet_show_map, name='template_4_1'),       #4章 Leaflet地図の表示
    url(r'^template_4_2/$', views.leaflet_configure_map, name='template_4_2'),  #4章 Leaflet地図の設定
    url(r'^template_4_3/$', views.leaflet_drawobject, name='template_4_3'),     #4章 Leaflet図形の描画
    url(r'^template_4_4/$', views.leaflet_popup, name='template_4_4'),          #4章 Leafletポップアップの設定
    url(r'^template_4_5/$', views.leaflet_with_temp, name='template_4_5'),      #4章 Leaflet Templateとの組み合わせ
    url(r'^template_4_6/$', views.leaflet_click_eve, name='template_4_6'),      #4章 Leaflet ユーザー操作の取得
    url(r'^template_4_7/$', views.leaflet_with_dbselect, name='template_4_7'),  #4章 Leaflet セレクトボックスから選択した情報を地図に表示
    url(r'^template_4_8/$', views.leaflet_update_DB, name='db_get_request'),    #4章 Leaflet 選択した座標の情報をデータベースに登録
    url(r'^db_get_request/$', views.db_get_request, name='db_get_request'),     #4章 Leaflet 選択した座標の情報をデータベースに登録　（AJAX用)
    #url(r'^submitted_to_dj/$', views.req_from_dj, name='req_from_dj'), #追加する(form説明用)
    #url(r'^template_for_dbtest/$', views.db_test, name='db_test'),     # 追加する
    # Geojson
    url(r'^station_info.geojson$', GeoJSONLayerView.as_view(model=Station_Info_MODEL), name='station_info'), 
    url(r'^template_for_LeafletDB/$', views.Leaflet_DB, name='Leaflet_DB'),  # 追加する

]
