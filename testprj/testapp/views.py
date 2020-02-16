from django.shortcuts import render
from django.http import HttpResponse
from testapp.models import Station_MODEL               #modelsに記述したクラス名に合わせる
from testapp.forms import  Custom_form  #modelChoiceField
import json
import datetime

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


def Leaflet_DB(request):
  choicefieldform = Custom_form()
  if request.method == 'GET':
    pass
  d = {
    'choicefield_form':choicefieldform
  }
  return render(request, 'template.html', d)


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



# 3章 ラジオボタン/チェックボックス/セレクトボックスの実装
# def req_from_dj(request):
#   d = {
#     'res_submitted_to_dj': request.GET.get('submitted_to_dj'),
#     'res_q1': request.GET.get('q1'),
#     'res_q2': request.GET.get('q2'),
#     'res_eki': request.GET.get('eki'),
#     'res_rosen': request.GET.get('rosen'),
#     'res_example': request.GET.get('example')
#   }
#   print("response") #デバッグ用
#   print(d)
#   return render(request, 'template.html', d)

# 3章 データベースの表示
# def db_test(request):
#   #modelsの要素を取得
#   #modelから特定の列の要素をリストにして取得
#   mdl_data_all = Station_MODEL.objects.all()  #modelの全てのデータを取得 (データベースの登録順に表示)
#   #mdl_data_all = Station_MODEL.objects.all().order_by('id') #ID順をキーに昇順に並べる場合(必要に応じて設定)
#   name_list = list(Station_MODEL.objects.values_list('name', flat=True))  #python の1次元配列で特定の列を取得する
#   choicefieldform = Custom_form()
#   if request.method == 'GET':
#     aaa = request.GET.get('station_label')
#   d = {
#     'res_models_name_list': name_list,
#     'mdl_data_all':mdl_data_all,
#     'choicefield_form':choicefieldform
#   }
#   return render(request, 'template.html', d)