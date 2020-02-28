from django.shortcuts import render
from django.http import HttpResponse
from testapp.models import Station_MODEL               #modelsに記述したクラス名に合わせる
from testapp.forms import  Custom_form                 #modelChoiceField
from testapp.open_data_web_api import func_tokyo_public_trans_API #東京公共交通API
import json
import datetime
import numpy as np
import pandas as pd
import re
import pyproj   #座標変換用ライブラリ

#2章 Hello World
def hello(req):
  return HttpResponse('Hello, World !!')

#2章Templateを用いたWebページの開発
def hello_template(request):
  return render(request, 'template.html')

#3章HTML構造
def html_structure(request):
  return render(request, 'chap_3_1_HTML_structure_template.html')

#3章HTML_テキスト(Pタグ・Hタグ)
def html_text_p_h(request):
  return render(request, 'chap_3_2_HTML_P_H_template.html')

#3章HTML ハイパーリンク
def html_hyperlink(request):
  return render(request, 'chap_3_3_HTML_hyperlink_template.html')

#3章 HTML 画像表示
def html_image(request):
  return render(request, 'chap_3_4_HTML_image_template.html')

#3章 CSS (基本)
def css_basic(request):
  return render(request, 'chap_3_5_CSS_template.html')

#3章 CSS (ID指定)
def css_with_ID(request):
  return render(request, 'chap_3_6_CSS_with_ID_template.html')

#3章 CSSレイアウト
def css_with_Layout(request):
  return render(request, 'chap_3_7_HTML_CSS_layout_template.html')

#3章 フォーム (セレクトボックス・ラジオボタン・チェックボックス)
def html_webform(request):
  d = {
    'res_submitted_to_dj': request.GET.get('submitted_to_dj'),
    'res_q1': request.GET.get('q1'),
    'res_q2': request.GET.get('q2'),
    'res_eki': request.GET.get('eki'),
    'res_rosen': request.GET.get('rosen'),
    'res_example': request.GET.get('example')
  }
  print("response") #デバッグ用
  print(d)
  return render(request, 'chap_3_8_formbutton_template.html', d)

#3章 データベースの表示
def html_dbshowdata(request):
  #modelsの要素を取得
  #modelから特定の列の要素をリストにして取得
  mdl_data_all = Station_MODEL.objects.all()  #modelの全てのデータを取得 (データベースの登録順に表示)
  #mdl_data_all = Station_MODEL.objects.all().order_by('id') #ID順をキーに昇順に並べる場合(必要に応じて設定)
  name_list = list(Station_MODEL.objects.values_list('name', flat=True))  #python の1次元配列で特定の列を取得する
  if request.method == 'GET':
    aaa = request.GET.get('station_label')
  d = {
    'res_models_name_list': name_list,
    'mdl_data_all':mdl_data_all,
  }
  return render(request, 'chap_3_9_DBshow_data.html', d)


#3章 データベースをセレクトボックスに指定
def html_dbselectbox(request):
  choicefieldform = Custom_form()
  if request.method == 'GET':
    aaa = request.GET.get('station_label')
  d = {
    'choicefield_form':choicefieldform
  }
  return render(request, 'chap_3_10_DBselectbox.html', d)

#3章 データベースを更新
def db_test_update(request):
  res_message = ""
  if request.method == 'POST':
    req_ID = request.POST.get('Req_ID')
    req_StationName = request.POST.get('Req_Station_Name')
    req_Lat = request.POST.get('Req_Station_Lat')
    req_Lon = request.POST.get('Req_Station_Lon')
    print("REQESTED",req_ID,req_StationName,req_Lat,req_Lon)

    #DBへの登録
    try:
      chk_tmp = Station_MODEL.objects.update_or_create(dataid=req_ID,
            defaults={'name':req_StationName,'latitude':req_Lat, 'longitude':req_Lon})
      res_message = "データベースに正常に反映されました"
    except Exception as e:
      print("例外:", e.args)
      #res_message = "例外"+e.args
  d = {
    'res_message': res_message
  }
  return render(request, 'chap_3_11_DBupdate_template.html', d)
  

#4章 Leaflet地図の表示
def leaflet_show_map(request):
  return render(request, 'chap_4_1_Leaflet_simple_template.html')

#4章 Leaflet地図の設定
def leaflet_configure_map(request):
  return render(request, 'chap_4_2_Leaflet_config_template.html')

#4章 Leaflet図形の描画
def leaflet_drawobject(request):
  return render(request, 'chap_4_3_Leaflet_drawobject_template.html')

#4章 Leafletポップアップの設定
def leaflet_popup(request):
  return render(request, 'chap_4_4_Leaflet_popup_template.html')

#4章 Leaflet Templateとの組み合わせ
def leaflet_with_temp(request):
  return render(request, 'chap_4_5_Leaflet_with_temp_template.html')

#4章 Leaflet ユーザー操作の取得
def leaflet_click_eve(request):
  return render(request, 'chap_4_6_Leaflet_click_eve_template.html')

#4章 Leaflet セレクトボックスから選択した情報を地図に表示
def leaflet_with_dbselect(request):
  choicefieldform = Custom_form()
  if request.method == 'GET':
    pass
  d = {
    'choicefield_form':choicefieldform
  }
  return render(request, 'chap_4_7_Leaflet_with_DBselect_template.html', d)

#4章 Leaflet 選択した座標の情報をデータベースに登録
def leaflet_update_DB(request):
  choicefieldform = Custom_form()
  if request.method == 'GET':
    pass
  d = {
    'choicefield_form':choicefieldform
  }
  return render(request, 'chap_4_8_Leaflet_updateDB.html', d)

#4章 Leaflet 選択した座標の情報をデータベースに登録（AJAX用)
def db_get_request(request):
  if request.method == 'GET': #データ取得要求
    req_name = request.GET.get('clicked_station_name')
    #modelから駅名にマッチするデータを探索
    chk_tmp = Station_MODEL.objects.get(name=req_name)
    #結果をディクショナリ⇒JSON形式データに変換して返す
    response = {
      'lat':chk_tmp.latitude,
      'lon':chk_tmp.longitude,
    }
    response = json.dumps(response)
  elif request.method == 'POST': #データベース更新要求
    result = -1
    req_name = request.POST.get('name_req')
    req_lat = request.POST.get('clicked_lat_req')
    req_lon = request.POST.get('clicked_lon_req')
    #同じ名前のデータが含まれるときは登録しない
    try:
      chk_tmp = Station_MODEL.objects.get(name=req_name)
    except Station_MODEL.DoesNotExist:
        result = 1
    except Exception as e:  
        result = -1
    
    #存在しないときはデータを登録
    if result > 0:
        dt_temp = datetime.datetime.now() #固有IDを時間から作る 
        target_dataid =dt_temp.month*100000
        target_dataid =dt_temp.day*10000
        target_dataid =dt_temp.hour*1000
        target_dataid =dt_temp.minute*100
        target_dataid =dt_temp.second
        chk_tmp = Station_MODEL.objects.update_or_create(dataid=target_dataid,defaults={'name':req_name,'latitude':req_lat, 'longitude':req_lon})
    response = {
      'result':result,
    }
    response = json.dumps(response)
  else:
    response = ""
  return HttpResponse(response, content_type = 'application/json')

#5章 国土地理院地図情報の可視化
def show_gsi_mapdata(request):
  return render(request, 'chap_5_1_show_geojson_template.html')

#5章 東京公共交通API
def tokyo_pub_api(request):
  return render(request, 'chap_5_2_show_timetable_template.html')

#5章 東京公共交通API(AJAX)
def get_tokyo_api(request):
  if request.method == 'GET': #データ取得要求
    req_lat = request.GET.get('center_lat')
    req_lng = request.GET.get('center_lng')
    #東京公共交通APIからマップ中央から10km以内の座標を取得 (pandas)
    res_df = func_tokyo_public_trans_API().search_GPS_near_train_station_info(req_lat,req_lng,10000)

    #一つもヒットしなかった場合
    if len(res_df.index) == 0:
      response = json.dumps("")
      return HttpResponse(response, content_type = 'application/json')
    elif len(res_df.index) >= 5:
      #5件以上のデータを取得できた場合
      #要求座標から最短となる結果を取得
      #距離情報を計算 
      grs80 = pyproj.Geod(ellps='GRS80')  # GRS80楕円体
      np_result_lat = np.array(res_df["geo:lat"])
      np_result_lon = np.array(res_df["geo:long"])
      np_origin_lat = np.full_like(np_result_lat, req_lat)
      np_origin_lon = np.full_like(np_result_lat, req_lng)
      azimuth, bkw_azimuth, distance = grs80.inv(np_origin_lon, np_origin_lat, np_result_lon, np_result_lat)  
      #出発点からの角度(北から deg)、目標点の角度(北から deg)、直線距離(m)
      res_df['distance'] = distance
      sorted_df =  res_df.sort_values(by='distance', ascending=True)
      res_df =sorted_df[:5]
    else:
      pass      

    #要素を配列にまとめる
    lat_array = res_df['geo:lat'].tolist()    #駅緯度
    lon_array = res_df['geo:long'].tolist()   #駅経度
    dist_array = res_df['distance'].tolist()  #地図中央座標からの距離
    name_array = res_df['dc:title'].tolist()  #駅名
    operator_code_array = res_df['odpt:operator'].tolist()  #事業者コード
    railway_code_array = res_df['odpt:railway'].tolist()  #路線名
    Timetable_array = res_df['odpt:stationTimetable'].tolist()  #路線名

    #事業者名の取得
    operator_list = func_tokyo_public_trans_API().get_Operator_information()
    operator_name_array = []
    for indx in range(len(res_df.index)):
      operator_name = operator_list[operator_list["owl:sameAs"]==operator_code_array[indx]]  #駅名コードをリストから検索
      operator_name = operator_name["dc:title"].values  #駅名の取得
      operator_name_array.append(operator_name[0])

    #路線名の取得
    railway_name_array = []
    for indx in range(len(res_df.index)):
      railway_name =func_tokyo_public_trans_API().get_Train_Railway_information(railway_code = railway_code_array[indx])
      railway_name_array.append(operator_name_array[indx]+" "+railway_name['dc:title'].values[0]) #事業者名と路線名を結合

    #土日判定
    weekday = datetime.date.today().weekday()
    if weekday>=5:
      holiday_flg = True
    else:
      holiday_flg = False

    #現在時間の取得
    current_time = int(datetime.datetime.now().strftime('%H%M'))
    if current_time < 500:  #深夜5時以降は24時間換算
      current_time +=2400

    #タイムテーブルへのアクセス
    departure_time_array = []
    destination_array = []
    for indx in range(len(res_df.index)):
      departure_timeobj = []
      destination_timeobj = []
      for indx2 in range(len(Timetable_array[indx])):
        Checkflag = False
        timetable_code = Timetable_array[indx][indx2]
        #アクセス日が平日の場合
        if (holiday_flg == False) and (timetable_code.find("Weekday")>0):
          Checkflag = True
        elif (holiday_flg == True) and (timetable_code.find("Holiday")>0):
          Checkflag = True
        else:
          continue
        if Checkflag == True:
          statimetable = func_tokyo_public_trans_API().get_Train_Railway_StationTimetable_information(timetable_code=timetable_code)
          try:
            for ikisakiindx in range(len(statimetable["odpt:stationTimetableObject"].values)):
              for timetableindx in range(len(statimetable["odpt:stationTimetableObject"].values[ikisakiindx])):
                  temptime = statimetable["odpt:stationTimetableObject"].values[ikisakiindx][timetableindx]["odpt:departureTime"]
                  temptime = int(re.sub("\\D", "", temptime)) #数字のみを抽出
                  if temptime < 500:  #深夜5時以降は24時間換算
                    temptime_comp = temptime + 2400
                  else:
                    temptime_comp = temptime
                  if current_time < temptime_comp:
                    deststation_code =  statimetable["odpt:stationTimetableObject"].values[ikisakiindx][timetableindx]["odpt:destinationStation"][0]
                    destination_name_name =func_tokyo_public_trans_API().get_Train_Railway_Station_information(station_code = deststation_code)
                    departure_timeobj.append(temptime)
                    destination_timeobj.append(destination_name_name['dc:title'].values[0])
                    break
          except Exception as e:
            continue
      departure_time_array.append(departure_timeobj)
      destination_array.append(destination_timeobj)

    response = {
      'lat':lat_array,
      'lon':lon_array,
      'name':name_array,
      'distance':dist_array,
      'operator_name':railway_name_array,
      'departure_time_array':departure_time_array,
      'destination_array':destination_array,
    }
    response = json.dumps(response)
  return HttpResponse(response, content_type = 'application/json')
