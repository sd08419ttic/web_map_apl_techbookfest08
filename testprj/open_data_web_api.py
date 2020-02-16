#!/usr/bin/env python
# -*- coding: utf-8 -*-
#5章　東京公共交通オープンデータチャレンジ API
import requests
import json
import pandas as pd

#東京公共交通オープンデータチャレンジ API
class func_tokyo_public_trans_API():

    #初期化用クラス (変数の宣言/初期化)
    def __init__(self):
        #APIキー (公式サイトから受領したものを利用すること)
        self.consumerKey = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

        #URL 共通
        self.URL_common = 'https://api-tokyochallenge.odpt.org/api/v4/'

        #API 
        self.API_RESPONSE_SUCCESS = 200

        #APIレスポンスとメッセージ表
        self.resp_tbl = { 200:"正常終了",
                          400:"パラメータ不正",
                          401:"acl:consumerKeyが誤っている",
                          403:"権限なし",
                          404:"該当データ無し",
                          405:"許可されていないHTTP Method",
                          500:"サーバー内部エラー",
                          503:"サービス利用不可"}

        #DEBUGフラグ (csvに保存)
        self.DEB_FLAG = True

    #カレンダーの情報取得
    #2.2.1. GET /api/v4/odpt:Calendar

    #入力　(全てオプション APIキーは省略)
    #@id optional (データID)
    #owl:sameAs  (Weekday or Holiday or 曜日)

    def get_Calendar_information(self):
        RDF_TYPE = "odpt:Calendar"
        URL_REQ = self.URL_common + RDF_TYPE
        params = {'acl:consumerKey': self.consumerKey}
        response = requests.get(URL_REQ, params=params)
        print(response.status_code)
        df_s = pd.read_json(response.text, encoding="shift-jis")
        df_s.to_csv("get_Calendar_information.csv",encoding='utf_8_sig') #for debug


    #公共交通機関の事業者の情報取得
    #2.2.2. GET /api/v4/odpt:Operator

    #入力　(全てオプション APIキーは省略)
    #@id optional (データID)
    #owl:sameAs  (事業者固有識別子　odpt.Operator:JR-East　名称(日本語)はodpt:operatorTitle )

    def get_Operator_information(self):
        RDF_TYPE = "odpt:Operator"
        URL_REQ = self.URL_common + RDF_TYPE
        params = {'acl:consumerKey': self.consumerKey}
        response = requests.get(URL_REQ, params=params)
        print(response.status_code)
        df_s = pd.read_json(response.text, encoding="shift-jis")
        if self.DEB_FLAG == True:
            df_s.to_csv("get_Operator_information.csv",encoding='utf_8_sig') #for debug
        return df_s

    ###################
    ### 鉄道用 API ####
    ###################

    #駅の乗降人員数
    #3.2.1. GET /api/v4/odpt:PassengerSurvey

    #入力　(全てオプション APIキーは省略)
    #@id optional (データID)
    #owl:sameAs  (駅名固有識別子　"odpt.PassengerSurvey:JR-East.Tokyo"など)
    #odpt:operator (事業者名識別子"odpt.Operator:JR-East"など)
    #odpt:station (駅名固有識別子　"odpt.PassengerSurvey:JR-East.Tokyo"など)
    #odpt:odpt:railway  (路線名固有識別子　"odpt.Railway:JR-East.Yamanote"など)

    def get_Train_Passenger_information(self,operator="",station ="",railway=""):
        RDF_TYPE = "odpt:PassengerSurvey"
        URL_REQ = self.URL_common + RDF_TYPE
        params = {'acl:consumerKey': self.consumerKey}

        #検索条件が追加されている場合
        if operator != "":
            params.update({'odpt:operator':operator})

        if station != "":
            params.update({'odpt:station':station})

        if railway != "":
            params.update({'odpt:railway':railway})

        response = requests.get(URL_REQ, params=params)
        print(response.status_code)
        df_s = pd.read_json(response.text, encoding="shift-jis")
        if self.DEB_FLAG == True:
            df_s.to_csv("get_Train_Passenger_information.csv",encoding='utf_8_sig') #for debug
        return df_s

    #進行方向の定義を取得する
    #3.2.2. GET /api/v4/odpt:RailDirection

    #入力　(全てオプション APIキーは省略)
    #@id optional (データID)
    #owl:sameAs  (駅名固有識別子　"odpt.PassengerSurvey:JR-East.Tokyo"など)

    def get_Train_RailDirection_information(self):
        RDF_TYPE = "odpt:RailDirection"
        URL_REQ = self.URL_common + RDF_TYPE
        params = {'acl:consumerKey': self.consumerKey}

        response = requests.get(URL_REQ, params=params)
        print(response.status_code)
        df_s = pd.read_json(response.text, encoding="shift-jis")
        if self.DEB_FLAG == True:
            df_s.to_csv("get_Train_RailDirection_information.csv",encoding='utf_8_sig') #for debug
        return df_s


    #路線情報を取得する
    #3.2.3. GET /api/v4/odpt:Railway

    #入力　(全てオプション APIキーは省略)
    #@id optional (データID)
    #owl:sameAs  (路線固有識別子　"odpt.Railway:JR-East.HokurikuShinkansen"など)
    #dc:title    (路線名（e.g. 小田原線、京王線、相模原線))
    #odpt:operator   (運営会社固有識別　"odpt.Operator:Keikyu"など)
    #odpt:lineCode   (路線コード、路線シンボル表記（e.g. 小田原線 => OH、丸ノ内線 => M）)

    def get_Train_Railway_information(self,railway_code="",railway_name="",railway_operator="",railway_LINECODE=""):
        RDF_TYPE = "odpt:Railway"
        URL_REQ = self.URL_common + RDF_TYPE
        params = {'acl:consumerKey': self.consumerKey}


        #検索条件が追加されている場合
        if railway_code != "":  #路線固有識別子 odpt.Railway:JR-East.HokurikuShinkansen など
            params.update({'owl:sameAs':railway_code})

        if railway_name != "":  #路線名（e.g. 小田原線、京王線、相模原線)
            params.update({'dc:title':railway_name})

        if railway_operator != "":  #運営会社固有識別　"odpt.PassengerSurvey:JR-East.Tokyo"
            params.update({'odpt:operator':railway_operator})

        if railway_LINECODE != "":  #路線コード、路線シンボル表記（e.g. 小田原線 => OH、丸ノ内線 => M）
            params.update({'odpt:lineCode':railway_LINECODE})

        response = requests.get(URL_REQ, params=params)
        print(response.status_code)
        df_s = pd.read_json(response.text, encoding="shift-jis")
        if self.DEB_FLAG == True:
            df_s.to_csv("get_Train_Railway_information.csv",encoding='utf_8_sig') #for debug
        return df_s

    #2駅間の運賃を取得する。
    #3.2.4. GET /api/v4/odpt:RailwayFare

    #入力　(全てオプション APIキーは省略)
    #@id optional (データID)
    #owl:sameAs  (計算区間の固有識別子　"odpt.RailwayFare:TokyoMetro.Marunouchi.Tokyo.TokyoMetro.Tozai.Nakano"
    #odpt:operator   (運営会社固有識別子　"odpt.Operator:Keikyu"など)
    #odpt:fromStation  (計算開始駅固有識別子　など)
	#odpt:toStation  (計算終了駅固有識別子　など)

    def get_Train_Railway_Fare_information(self,fare_code="",operator_name="",from_sation_code="",to_sation_code=""):
        RDF_TYPE = "odpt:RailwayFare"
        URL_REQ = self.URL_common + RDF_TYPE
        params = {'acl:consumerKey': self.consumerKey}


        #検索条件が追加されている場合
        if fare_code != "":  #料金計算区間識別子
            params.update({'owl:sameAs':fare_code})

        if operator_name != "":  #路線名（e.g. 小田原線、京王線、相模原線)
            params.update({'odpt:operator':operator_name})

        if from_sation_code != "":  #計算開始駅固有識別子　"odpt.PassengerSurvey:JR-East.Tokyo"
            params.update({'odpt:fromStation':from_sation_code})

        if to_sation_code != "":  #計算終了駅固有識別子、路線シンボル表記（e.g. 小田原線 => OH、丸ノ内線 => M）
            params.update({'odpt:toStation':to_sation_code})

        response = requests.get(URL_REQ, params=params)
        print(response.status_code)
        df_s = pd.read_json(response.text, encoding="shift-jis")

        if self.DEB_FLAG == True:
            df_s.to_csv("get_Train_Railway_Fare_information.csv",encoding='utf_8_sig') #for debug
        return df_s


    #駅情報を取得する
    #3.2.5. GET /api/v4/odpt:Station

    #入力　(全てオプション APIキーは省略)
    #@id optional (データID)
    #owl:sameAs  (駅名の固有識別子　"odpt.RailwayFare:TokyoMetro.Marunouchi.Tokyo.TokyoMetro.Tozai.Nakano"
    #dc:title    (駅名(e.g. 東京、新宿、上野))
    #odpt:operator   (運営会社固有識別子　"odpt.Operator:Keikyu"など)
    #odpt:railway  (路線名固有識別子　"odpt.Railway:JR-East.Yamanote"など)
    #odpt:stationCode  駅ナンバリング（e.g. OH01=小田急新宿駅）

    def get_Train_Railway_Station_information(self,station_code="",station_name="",operator_code="",railway_code="",station_numcode=""):
        RDF_TYPE = "odpt:Station"
        URL_REQ = self.URL_common + RDF_TYPE
        params = {'acl:consumerKey': self.consumerKey}

        #検索条件が追加されている場合
        if station_code != "":  #料金計算区間識別子
            params.update({'owl:sameAs':station_code})

        if station_name != "":  #駅名（e.g. 渋谷、品川)
            params.update({'dc:title':station_name})

        if operator_code != "":  #運営会社固有識別子　"odpt.PassengerSurvey:JR-East.Tokyo"
            params.update({'odpt:operator':operator_code})

        if railway_code != "":  #計算終了駅固有識別子、路線シンボル表記（e.g. 小田原線 => OH、丸ノ内線 => M）
            params.update({'odpt:railway':railway_code})

        if station_numcode != "":  #計算終了駅固有識別子、路線シンボル表記（e.g. 小田原線 => OH、丸ノ内線 => M）
            params.update({'odpt:stationCode':station_numcode})


        response = requests.get(URL_REQ, params=params)
        print(response.status_code)
        df_s = pd.read_json(response.text, encoding="shift-jis")

        if self.DEB_FLAG == True:
            df_s.to_csv("get_Train_Railway_Station_information.csv",encoding='utf_8_sig') #for debug
        return df_s

    #駅時刻表を取得する
    #3.2.6. GET /api/v4/odpt:StationTimetable

    #入力　(全てオプション APIキーは省略)
    #@id optional (データID)
    #owl:sameAs (駅名の固有識別子)
    #odpt:station (駅名固有識別子　"odpt.PassengerSurvey:JR-East.Tokyo"など)
    #odpt:odpt:railway  (路線名固有識別子　"odpt.Railway:JR-East.Yamanote"など)
    #odpt:operator (事業者名識別子"odpt.Operator:JR-East"など)
    #odpt:railDirection(列車進行方向　.Outbound　など) 
    #odpt:odpt:calendar(カレンダー　平日/休日などodpt.Calendar:Weekday)
    #dc:date :(日付　"2017-01-13T15:10:00+09:00")

    def get_Train_Railway_StationTimetable_information(self,timetable_code="",station_code="",station_name="",operator_code="",railway_code="",station_numcode=""):
        RDF_TYPE = "odpt:StationTimetable"
        URL_REQ = self.URL_common + RDF_TYPE
        params = {'acl:consumerKey': self.consumerKey}

        #検索条件が追加されている場合
        if station_code != "":  #駅名識別子
            params.update({'odpt:station':station_code})

        if station_name != "":  #駅名（e.g. 渋谷、品川)
            params.update({'dc:title':station_name})

        if operator_code != "":  #運営会社固有識別子　"odpt.PassengerSurvey:JR-East.Tokyo"
            params.update({'odpt:operator':operator_code})

        if railway_code != "":  #計算終了駅固有識別子、路線シンボル表記（e.g. 小田原線 => OH、丸ノ内線 => M）
            params.update({'odpt:railway':railway_code})

        if station_numcode != "":  #計算終了駅固有識別子、路線シンボル表記（e.g. 小田原線 => OH、丸ノ内線 => M）
            params.update({'odpt:stationCode':station_numcode})


        response = requests.get(URL_REQ, params=params)
        print(response.status_code)
        df_s = pd.read_json(response.text, encoding="shift-jis")

        if self.DEB_FLAG == True:
            df_s.to_csv("get_Train_Railway_StationTimetable_information.csv",encoding='utf_8_sig') #for debug
        return df_s

    #列車情報(列車の位置情報)を取得する
    #3.2.7. GET /api/v4/odpt:Train

    #入力　(全てオプション APIキーは省略)
    #owl:sameAs (列車の固有識別子)
    #odpt:operator (事業者名識別子"odpt.Operator:JR-East"など)
    #odpt:odpt:railway  (路線名固有識別子　"odpt.Railway:JR-East.Yamanote"など)

    def get_Train_Railway_Train_information(self,train_code="",operator_code="",railway_code=""):
        RDF_TYPE = "odpt:Train"
        URL_REQ = self.URL_common + RDF_TYPE
        params = {'acl:consumerKey': self.consumerKey}

        #検索条件が追加されている場合
        if train_code != "":  #列車名識別子
            params.update({'owl:sameAs':train_code})

        if operator_code != "":  #運営会社固有識別子　"odpt.PassengerSurvey:JR-East.Tokyo"
            params.update({'odpt:operator':operator_code})

        if railway_code != "":  #計算終了駅固有識別子、路線シンボル表記（e.g. 小田原線 => OH、丸ノ内線 => M）
            params.update({'odpt:railway':railway_code})

        response = requests.get(URL_REQ, params=params)
        print(response.status_code)
        df_s = pd.read_json(response.text, encoding="shift-jis")

        if self.DEB_FLAG == True:
            df_s.to_csv("get_Train_Railway_Train_information.csv",encoding='utf_8_sig') #for debug
        return df_s

    #列車運行情報を取得する。
    #3.2.8. GET /api/v4/odpt:TrainInformation

    #入力　(全てオプション APIキーは省略)
    #owl:sameAs (固有識別子)
    #odpt:operator (事業者名識別子"odpt.Operator:JR-East"など)
    #odpt:odpt:railway  (路線名固有識別子　"odpt.Railway:JR-East.Yamanote"など)

    def get_Train_Railway_Train_Delay_information(self,traininfo_code="",operator_code="",railway_code=""):
        RDF_TYPE = "odpt:TrainInformation"
        URL_REQ = self.URL_common + RDF_TYPE
        params = {'acl:consumerKey': self.consumerKey}

        #検索条件が追加されている場合
        if traininfo_code != "":  #列車運行情報識別子
            params.update({'owl:sameAs':traininfo_code})

        if operator_code != "":  #運営会社固有識別子　"odpt.PassengerSurvey:JR-East.Tokyo"
            params.update({'odpt:operator':operator_code})

        if railway_code != "":  #計算終了駅固有識別子、路線シンボル表記（e.g. 小田原線 => OH、丸ノ内線 => M）
            params.update({'odpt:railway':railway_code})

        response = requests.get(URL_REQ, params=params)
        print(response.status_code)
        df_s = pd.read_json(response.text, encoding="shift-jis")

        if self.DEB_FLAG == True:
            df_s.to_csv("get_Train_Railway_Train_Delay_information.csv",encoding='utf_8_sig') #for debug
        return df_s

    #列車時刻表を取得する。
    #3.2.9. GET /api/v4/odpt:TrainTimetable

    #入力　(全てオプション APIキーは省略)
    #owl:sameAs (固有識別子)
    #odpt:trainNumber   (路線番号固有識別子　""565M"など)
    #odpt:railway  (路線名固有識別子　"odpt.Railway:JR-East.Yamanote"など)
    #odpt:operator (事業者名識別子"odpt.Operator:JR-East"など)
    #odpt:trainType (列車種別　odpt.TrainType:JR-East.Rapid など)
    #odpt:train (列車固有識別子　.　など) 
    #odpt:calendar(カレンダー　平日/休日などodpt.Calendar:Weekday)

    def get_Train_Railway_TrainTimetable_information(self,traintimetable_code="",trainNumber="",railway_code="",operator_code="",trainType_code="",calender=""):
        RDF_TYPE = "odpt:TrainTimetable"
        URL_REQ = self.URL_common + RDF_TYPE
        params = {'acl:consumerKey': self.consumerKey}

        #検索条件が追加されている場合
        if traintimetable_code != "":  #列車タイムテーブル情報識別子
            params.update({'owl:sameAs':traintimetable_code})

        if trainNumber!="":  #列車番号
            params.update({'odpt:trainNumber':trainNumber})

        if railway_code != "":  #計算終了駅固有識別子、路線シンボル表記（e.g. 小田原線 => OH、丸ノ内線 => M）
            params.update({'odpt:railway':railway_code})

        if operator_code != "":  #運営会社固有識別子　"odpt.PassengerSurvey:JR-East.Tokyo"
            params.update({'odpt:operator':operator_code})

        if trainType_code != "":  #列車種別固有識別子
            params.update({'odpt:trainType':trainType_code})

        if calender != "":  #カレンダー情報
            params.update({'odpt:calendar':calender})

        response = requests.get(URL_REQ, params=params)
        print(response.status_code)
        df_s = pd.read_json(response.text, encoding="shift-jis")

        if self.DEB_FLAG == True:
            df_s.to_csv("get_Train_Railway_TrainTimetable_information.csv",encoding='utf_8_sig') #for debug
        return df_s


    #列車種別の定義を取得する。
    #3.2.10. GET /api/v4/odpt:TrainType

    #入力　(全てオプション APIキーは省略)
    #owl:sameAs (固有識別子)
    #odpt:operator (事業者名識別子"odpt.Operator:JR-East"など)

    def get_Train_Railway_TrainType_information(self,traintype_code="",operator_code=""):
        RDF_TYPE = "odpt:TrainType"
        URL_REQ = self.URL_common + RDF_TYPE
        params = {'acl:consumerKey': self.consumerKey}

        #検索条件が追加されている場合
        if traintype_code != "":  #列車タイムテーブル情報識別子
            params.update({'owl:sameAs':traintimetable_code})

        if operator_code != "":  #運営会社固有識別子　"odpt.PassengerSurvey:JR-East.Tokyo"
            params.update({'odpt:operator':operator_code})

        response = requests.get(URL_REQ, params=params)
        print(response.status_code)
        df_s = pd.read_json(response.text, encoding="shift-jis")

        if self.DEB_FLAG == True:
            df_s.to_csv("get_Train_Railway_TrainType_information.csv",encoding='utf_8_sig') #for debug
        return df_s

    #################
    ### バス API ####
    #################

    #バス車両の運行情報(odpt:Bus)を取得する。
    #4.2.1. GET /api/v4/odpt:Bus

    #入力　(全てオプション APIキーは省略)
    #owl:sameAs (固有識別子)
    #odpt:busroutePattern    (バスの運行系統のID )
    #odpt:operator (事業者名識別子"など)
    #odpt:fromBusstopPole  (直近に通過したバス停のID)
    #oodpt:toBusstopPole (次に通過するバス停のID)

    def get_Bus_Bus_CurrentOperation_information(self,bus_oper_code="",busroutePattern_code="",operator_code="",fromBusstopPole_code="",toBusstopPole_code=""):
        RDF_TYPE = "odpt:Bus"
        URL_REQ = self.URL_common + RDF_TYPE
        params = {'acl:consumerKey': self.consumerKey}

        #検索条件が追加されている場合
        if bus_oper_code != "":  #バス検索コード　odpt.Bus:Toei.To07.60101.1.V389
            params.update({'owl:sameAs':bus_oper_code})

        if busroutePattern_code != "":  #バスの運行系統のID
            params.update({'odpt:busroutePattern':busroutePattern_code})

        if operator_code != "":
            params.update({'odpt:operator':operator_code})

        if fromBusstopPole_code != "":
            params.update({'odpt:fromBusstopPole':fromBusstopPole_code})

        if toBusstopPole_code != "":
            params.update({'odpt:toBusstopPole':toBusstopPole_code})

        response = requests.get(URL_REQ, params=params)
        print(response.status_code)
        df_s = pd.read_json(response.text, encoding="shift-jis")

        if self.DEB_FLAG == True:
            df_s.to_csv("get_Bus_Bus_CurrentOperation_information.csv",encoding='utf_8_sig') #for debug
        return df_s

    #バス時刻表(odpt:BusTimetable)の取得
    #4.2.2. GET /api/v4/odpt:BusTimetable

    #入力　(全てオプション APIキーは省略)
    #owl:sameAs (バス時刻表固有識別子)
    #odpt:operator (事業者名識別子"など)
    #odpt:busroutePattern    (バスの運行系統のID )
    #dc:title   (バス路線名)
    #odpt:calendar  (カレンダーのID)

    def get_Bus_BusTimetable_information(self,bus_ttable_code="",operator_code="",busroutePattern_code="",bus_routetiltle="",calender_code=""):
        RDF_TYPE = "odpt:BusTimetable"
        URL_REQ = self.URL_common + RDF_TYPE
        params = {'acl:consumerKey': self.consumerKey}

        #検索条件が追加されている場合
        if bus_ttable_code != "":  #バス時刻表コード
            params.update({'owl:sameAs':bus_ttable_code})

        if operator_code != "": #バス事業者ID
            params.update({'odpt:operator':operator_code})

        if busroutePattern_code != "":  #バスの運行系統のID
            params.update({'odpt:busroutePattern':busroutePattern_code})

        if bus_routetiltle != "":
            params.update({'dc:title':bus_routetiltle})

        if calender_code != "":
            params.update({'odpt:calendar':calender_code})

        response = requests.get(URL_REQ, params=params)
        print(response.status_code)
        df_s = pd.read_json(response.text, encoding="shift-jis")

        if self.DEB_FLAG == True:
            df_s.to_csv("get_Bus_BusTimetable_information.csv",encoding='utf_8_sig') #for debug
        return df_s


    #運行系統情報(odpt:BusroutePattern)の取得
    #4.2.3. GET /api/v4/odpt:BusroutePattern

    #入力　(全てオプション APIキーは省略)
    #owl:sameAs (バスの運行系統のID)
    #dc:title   (バス路線名)
    #odpt:operator (事業者名識別子"など)
    #odpt:busroutePattern    (バスの運行系統のID:　owlと同様なので実装を省略)

    def get_Bus_BusroutePattern_information(self,bus_routepattern_code="",route_title="",operator_code=""):
        RDF_TYPE = "odpt:BusroutePattern"
        URL_REQ = self.URL_common + RDF_TYPE
        params = {'acl:consumerKey': self.consumerKey}

        #検索条件が追加されている場合
        if bus_routepattern_code != "":  #バス時刻表コード
            params.update({'owl:sameAs':bus_routepattern_code})

        if route_title != "":
            params.update({'dc:title':route_title})

        if operator_code != "":  #バスの運行系統のID
            params.update({'odpt:operator':operator_code})

        response = requests.get(URL_REQ, params=params)
        print(response.status_code)
        df_s = pd.read_json(response.text, encoding="shift-jis")

        if self.DEB_FLAG == True:
            df_s.to_csv("get_Bus_BusroutePattern_information.csv",encoding='utf_8_sig') #for debug
        return df_s

    #運賃情報(odpt:BusroutePatternFare)の取得
    #4.2.4. GET /api/v4/odpt:BusroutePatternFare

    #入力　(全てオプション APIキーは省略)
    #owl:sameAs (バスの料金計算結果の固有識別子)
    #odpt:operator (事業者名識別子"など)
    #odpt:fromBusstopPole (乗車地点のバス停ID)
    #odpt:toBusstopPole (降車地点のバス停ID)
    #odpt:ticketFare (切符利用時の運賃)	
    #odpt:childTicketFare (切符利用時の子供運賃)
    #odpt:icCardFare  (切符利用時の運賃)
    #odpt:childIcCardFare   (IC利用時の子供運賃)

    def get_Bus_BusroutePatternFare_information(self,bus_routepatternfare_code="",operator_code="",from_pole_code="",to_pole_code=""):
        RDF_TYPE = "odpt:BusroutePatternFare"
        URL_REQ = self.URL_common + RDF_TYPE
        params = {'acl:consumerKey': self.consumerKey}

        #検索条件が追加されている場合
        if bus_routepatternfare_code != "":  #バスの料金計算結果の固有識別子
            params.update({'owl:sameAs':bus_routepatternfare_code})

        if operator_code != "":  #バスの運行系統のID
            params.update({'odpt:operator':operator_code})

        if from_pole_code != "":    #乗車バス停のID
            params.update({'odpt:fromBusstopPole':from_pole_code})

        if to_pole_code != "":    #降車バス停のID
            params.update({'odpt:fromBusstopPole':from_pole_code})


        response = requests.get(URL_REQ, params=params)
        print(response.status_code)
        df_s = pd.read_json(response.text, encoding="shift-jis")

        if self.DEB_FLAG == True:
            df_s.to_csv("get_Bus_BusroutePatternFare_information.csv",encoding='utf_8_sig') #for debug
        return df_s

    #4.2.5. GET /api/v4/odpt:BusstopPole
    #バス停(標柱)(odpt:BusstopPole)の取得

    #入力　(全てオプション APIキーは省略)
    #owl:sameAs (バス停(標柱)のID(odpt:BusstopPole owl:sameAs))
    #dc:title (停留所名称(odpt:BusstopPole dc:title)) 
    #odpt:busstopPoleNumber  (乗車地点のバス停ID)
    #odpt:busroutePattern  (標柱で発着する系統のID)
    #odpt:operator (事業者名識別子"など)

    def get_Bus_BusstopPole_information(self,bus_stoppole_code="",bus_stop_name="",busroutePattern_code="",operator_code=""):
        RDF_TYPE = "odpt:BusstopPole"
        URL_REQ = self.URL_common + RDF_TYPE
        params = {'acl:consumerKey': self.consumerKey}

        #検索条件が追加されている場合
        if bus_stoppole_code != "":  #バスの料金計算結果の固有識別子
            params.update({'owl:sameAs':bus_stoppole_code})

        if bus_stop_name != "":    #乗車バス停の名称
            params.update({'dc:title':bus_stop_name})

        if busroutePattern_code != "":    #降車バス停のID
            params.update({'odpt:busroutePattern':busroutePattern_code})

        if operator_code != "":  #バスの運行系統のID
            params.update({'odpt:operator':operator_code})


        response = requests.get(URL_REQ, params=params)
        print(response.status_code)
        df_s = pd.read_json(response.text, encoding="shift-jis")

        if self.DEB_FLAG == True:
            df_s.to_csv("get_Bus_BusstopPole_information.csv",encoding='utf_8_sig') #for debug
        return df_s

    #4.2.6. GET /api/v4/odpt:BusstopPoleTimetable
    #バス停(標柱)時刻表(odpt:BusstopPoleTimetable) の取得

    #入力　(全てオプション APIキーは省略)
    #owl:sameAs (バス停(標柱)のID(odpt:BusstopPole owl:sameAs))
    #odpt:busstopPole   (時刻表の対応するバス停(標柱)のID )
    #odpt:busDirection  (方面のID )
    #odpt:busroute  (路線ID)
    #odpt:operator (事業者名識別子"など)
    #odpt:calendar  (カレンダーのID)
    #dc:date  (カレンダーのID)

    def get_Bus_BusstopPoleTimetable_information(self,busstop_timetbl_code="",bus_stoppole_code="",busDirection_code="",busroute_code="",operator_code="",calendar_code="",date_num =""):
        RDF_TYPE = "odpt:BusstopPoleTimetable"
        URL_REQ = self.URL_common + RDF_TYPE
        params = {'acl:consumerKey': self.consumerKey}

        #検索条件が追加されている場合
        if busstop_timetbl_code !="":
            params.update({'owl:sameAs':busstop_timetbl_code})

        if bus_stoppole_code != "":  #バスの料金計算結果の固有識別子
            params.update({'odpt:busstopPole ':bus_stoppole_code})

        if busDirection_code != "":    #バスの進行方向コード
            params.update({'odpt:busDirection':busDirection_code})

        if busroute_code != "":    #乗車ルートのコード
            params.update({'odpt:busroute':busroute_code})

        if operator_code != "":  #バスの運行系統のID
            params.update({'odpt:operator':operator_code})

        if calendar_code != "":    #降車バス停のID
            params.update({'odpt:calendar':calendar_code})

        if date_num != "":    #降車バス停のID
            params.update({'dc:date':date_num})

        response = requests.get(URL_REQ, params=params)
        print(response.status_code)
        df_s = pd.read_json(response.text, encoding="shift-jis")

        if self.DEB_FLAG == True:
            df_s.to_csv("get_Bus_BusstopPoleTimetable_information.csv",encoding='utf_8_sig') #for debug
        return df_s

    #########################
    ### データダンプ API ####
    #########################

    #1.5. データダンプAPI (/v4/RDF_TYPE.json?)
    #各種データのダンプ (全件取得/ 検索APIだと1000件までしか出力されないため)
    #該当パラメータ
    #共通	odpt:Calendar	曜日・日付区分	曜日・日付区分が記述される
    #共通	odpt:Operator	事業者	公共交通機関の事業者が記述される
    #鉄道	odpt:Station	駅情報	駅の名称や位置など、駅に関連する情報が記述される
    #鉄道	odpt:StationTimetable	駅時刻表	駅を発着する列車の時刻表情報が記述される
    #鉄道	odpt:TrainTimetable	列車時刻表	列車がどの駅にいつ到着するか、出発するかが記述される
    #鉄道	odpt:TrainType	列車種別	普通、快速など、列車の種別を定義する
    #鉄道	odpt:RailDirection	進行方向	上り、下りなど、列車の進行方向を定義する
    #鉄道	odpt:Railway	路線情報	鉄道における路線、運行系統が記述される
    #鉄道	odpt:RailwayFare	運賃情報	鉄道の運賃が記述される
    #鉄道	odpt:PassengerSurvey	駅別乗降人員	駅の乗降数集計結果が記述される
    #バス	odpt:BusTimetable	バス時刻表	バスがあるバス停、バス標柱にいつ到着するか、いつ出発するかが記述される e.g. 系統時刻表、スターフ、運行表
    #バス	odpt:BusroutePattern	バス運行路線情報	バス運行における運行路線情報が記述される
    #バス	odpt:BusroutePatternFare	バス運賃情報	バスの運賃が記述される
    #バス	odpt:BusstopPole	バス停標柱情報	バス停における標柱情報が記述される
    #バス	odpt:BusstopPoleTimetable	バス停標柱時刻表	バスがあるバス停標柱にいつ到着するか、出発するかが記述される e.g. バス停時刻表、標柱時刻表、標柱
    #航空機	odpt:Airport	空港情報	空港の名称や位置など、空港に関連する情報が記述される
    #航空機	odpt:AirportTerminal	空港ターミナル情報	空港のターミナルの名称など、空港のターミナルに関連する情報が記述される
    #航空機	odpt:FlightSchedule	フライト時刻表	航空機の予定される発着時刻情報が記述される e.g. 月間時刻表、週間スケジュール
    #航空機	odpt:FlightStatus	フライト状況	空港を発着する航空機の状況を定義する

    def dump_Common_information(self):
        DUMP_REQ = ".json"
        params = {'acl:consumerKey': self.consumerKey}

        RDF_TYPE = "odpt:Calendar"  #カレンダー情報
        URL_REQ = self.URL_common + RDF_TYPE + DUMP_REQ
        response = requests.get(URL_REQ, params=params)
        df_s = pd.read_json(response.text, encoding="shift-jis")
        df_s.to_csv("dump_Common_information_Calender.csv",encoding='utf_8_sig') #for debug
        print(response.status_code,RDF_TYPE)


        RDF_TYPE = "odpt:Operator"  #事業者情報
        URL_REQ = self.URL_common + RDF_TYPE + DUMP_REQ
        response = requests.get(URL_REQ, params=params)
        df_s = pd.read_json(response.text, encoding="shift-jis")
        df_s.to_csv("dump_Common_information_Operator.csv",encoding='utf_8_sig') #for debug
        print(response.status_code,RDF_TYPE)

        return

    def dump_Train_information(self):
        DUMP_REQ = ".json"
        params = {'acl:consumerKey': self.consumerKey}

        RDF_TYPE = "odpt:Station"  #駅情報
        URL_REQ = self.URL_common + RDF_TYPE + DUMP_REQ
        response = requests.get(URL_REQ, params=params)
        df_s = pd.read_json(response.text, encoding="shift-jis")
        df_s.to_csv("dump_Train_information_Station.csv",encoding='utf_8_sig') #for debug
        print(response.status_code,RDF_TYPE)

        RDF_TYPE = "odpt:StationTimetable"  #駅時刻表
        URL_REQ = self.URL_common + RDF_TYPE + DUMP_REQ
        response = requests.get(URL_REQ, params=params)
        df_s = pd.read_json(response.text, encoding="shift-jis")
        df_s.to_csv("dump_Train_information_StationTimetable.csv",encoding='utf_8_sig') #for debug
        print(response.status_code,RDF_TYPE)

        RDF_TYPE = "odpt:TrainTimetable"  #列車時刻表
        URL_REQ = self.URL_common + RDF_TYPE + DUMP_REQ
        response = requests.get(URL_REQ, params=params)
        df_s = pd.read_json(response.text, encoding="shift-jis")
        df_s.to_csv("dump_Train_information_TrainTimetable.csv",encoding='utf_8_sig') #for debug
        print(response.status_code,RDF_TYPE)

        RDF_TYPE = "odpt:TrainType"  #列車種別
        URL_REQ = self.URL_common + RDF_TYPE + DUMP_REQ
        response = requests.get(URL_REQ, params=params)
        df_s = pd.read_json(response.text, encoding="shift-jis")
        df_s.to_csv("dump_Train_information_TrainType.csv",encoding='utf_8_sig') #for debug
        print(response.status_code,RDF_TYPE)

        RDF_TYPE = "odpt:RailDirection"  #列車進行方向
        URL_REQ = self.URL_common + RDF_TYPE + DUMP_REQ
        response = requests.get(URL_REQ, params=params)
        df_s = pd.read_json(response.text, encoding="shift-jis")
        df_s.to_csv("dump_Train_information_RailDirection.csv",encoding='utf_8_sig') #for debug
        print(response.status_code,RDF_TYPE)

        RDF_TYPE = "odpt:Railway"  #列車進行方向
        URL_REQ = self.URL_common + RDF_TYPE + DUMP_REQ
        response = requests.get(URL_REQ, params=params)
        df_s = pd.read_json(response.text, encoding="shift-jis")
        df_s.to_csv("dump_Train_information_Railway.csv",encoding='utf_8_sig') #for debug
        print(response.status_code,RDF_TYPE)

        RDF_TYPE = "odpt:Railway"  #路線情報
        URL_REQ = self.URL_common + RDF_TYPE + DUMP_REQ
        df_s = pd.read_json(response.text, encoding="shift-jis")
        df_s.to_csv("dump_Train_information_Railway.csv",encoding='utf_8_sig') #for debug
        print(response.status_code,RDF_TYPE)

        RDF_TYPE = "odpt:RailwayFare"  #運賃情報
        URL_REQ = self.URL_common + RDF_TYPE + DUMP_REQ
        response = requests.get(URL_REQ, params=params)
        df_s = pd.read_json(response.text, encoding="shift-jis")
        df_s.to_csv("dump_Train_information_RailwayFare.csv",encoding='utf_8_sig') #for debug
        print(response.status_code,RDF_TYPE)

        RDF_TYPE = "odpt:PassengerSurvey"  #運賃情報
        URL_REQ = self.URL_common + RDF_TYPE + DUMP_REQ
        response = requests.get(URL_REQ, params=params)
        df_s = pd.read_json(response.text, encoding="shift-jis")
        df_s.to_csv("dump_Train_information_PassengerSurvey.csv",encoding='utf_8_sig') #for debug
        print(response.status_code,RDF_TYPE)

        return

    def dump_Bus_information(self):
        DUMP_REQ = ".json"
        params = {'acl:consumerKey': self.consumerKey}

        RDF_TYPE = "odpt:BusTimetable"  #バス時刻表
        URL_REQ = self.URL_common + RDF_TYPE + DUMP_REQ
        response = requests.get(URL_REQ, params=params)
        df_s = pd.read_json(response.text, encoding="shift-jis")
        df_s.to_csv("dump_Bus_information_BusTimetable.csv",encoding='utf_8_sig') #for debug
        print(response.status_code,RDF_TYPE)


        RDF_TYPE = "odpt:BusroutePattern"  #バス運行路線情報
        URL_REQ = self.URL_common + RDF_TYPE + DUMP_REQ
        response = requests.get(URL_REQ, params=params)
        df_s = pd.read_json(response.text, encoding="shift-jis")
        df_s.to_csv("dump_Bus_information_BusroutePattern.csv",encoding='utf_8_sig') #for debug
        print(response.status_code,RDF_TYPE)

        RDF_TYPE = "odpt:BusroutePatternFare"  #バス運賃情報
        URL_REQ = self.URL_common + RDF_TYPE + DUMP_REQ
        response = requests.get(URL_REQ, params=params)
        df_s = pd.read_json(response.text, encoding="shift-jis")
        df_s.to_csv("dump_Bus_information_BusroutePatternFare.csv",encoding='utf_8_sig') #for debug
        print(response.status_code,RDF_TYPE)

        RDF_TYPE = "odpt:BusstopPole"  #バス停標柱情報
        URL_REQ = self.URL_common + RDF_TYPE + DUMP_REQ
        response = requests.get(URL_REQ, params=params)
        df_s = pd.read_json(response.text, encoding="shift-jis")
        df_s.to_csv("dump_Bus_information_BusstopPole.csv",encoding='utf_8_sig') #for debug
        print(response.status_code,RDF_TYPE)

        RDF_TYPE = "odpt:BusstopPoleTimetable"  #バス停標柱時刻表
        URL_REQ = self.URL_common + RDF_TYPE + DUMP_REQ
        response = requests.get(URL_REQ, params=params)
        df_s = pd.read_json(response.text, encoding="shift-jis")
        df_s.to_csv("dump_Bus_information_BusstopPoleTimetable.csv",encoding='utf_8_sig') #for debug
        print(response.status_code,RDF_TYPE)

        return

    ########################
    ### 地物情報検索 API ###
    ########################


    #1.7. 地物情報検索API 
    #GPS入力座標近辺にある電車/バス情報の取得

    #入力　(全て必須。駅/バスのどちらかのみを検索する設定のみ任意)
    #st_lat   (取得する範囲の中心緯度を指定、10進数表記、測地系はWGS84)
    #st_lon   (取得する範囲の中心経度を指定、10進数表記、測地系はWGS84)
    #radius_m  (取得する範囲の半径をメートルで指定、0-4000mの範囲 )
    #st_name  (駅名を日本語で指定)
    #operator_code (事業者コード名)
    #railway_code (路線コード名)

    #GPS座標で近隣に存在する駅の取得
    def search_GPS_near_train_station_info(self,st_lat="",st_lon="",radius_m="",st_name="",operator_code="",railway_code=""):
        RDF_TYPE = "places/odpt:Station?"
        URL_REQ = self.URL_common + RDF_TYPE
        params = {'acl:consumerKey': self.consumerKey}

        #検索条件が追加されている場合
        if st_lat !="":
            params.update({'lat':st_lat})
        if st_lon !="":
            params.update({'lon':st_lon})
        if radius_m !="":
            params.update({'radius':radius_m})
        if st_name !="":
            params.update({'dc:title':st_name})
        if operator_code !="":
            params.update({'odpt:operator':operator_code})
        if railway_code !="":
            params.update({'odpt:railway':railway_code})

        #odpt:railway

        response = requests.get(URL_REQ, params=params)
        print(response.status_code)
        df_s = pd.read_json(response.text)
        if self.DEB_FLAG == True:
            df_s_deb = pd.read_json(response.text, encoding="shift-jis")
            df_s_deb.to_csv("search_GPS_near_train_station_info.csv",encoding='utf_8_sig') #for debug

        print(df_s['odpt:operator'])

        return df_s

    #GPS座標で近隣に存在するバス停の取得
    def search_GPS_near_bus_station_info(self,st_lat="",st_lon="",radius_m="",st_name="",operator_code="",railway_code=""):
        RDF_TYPE = "places/odpt:BusstopPole?"
        URL_REQ = self.URL_common + RDF_TYPE
        params = {'acl:consumerKey': self.consumerKey}

        #検索条件が追加されている場合
        if st_lat !="":
            params.update({'lat':st_lat})
        if st_lon !="":
            params.update({'lon':st_lon})
        if radius_m !="":
            params.update({'radius':radius_m})
        if st_name !="":
            params.update({'dc:title':st_name})
        if operator_code !="":
            params.update({'odpt:operator':operator_code})
        if railway_code !="":
            params.update({'odpt:railway':railway_code})

        #odpt:railway

        response = requests.get(URL_REQ, params=params)
        print(response.status_code)
        df_s = pd.read_json(response.text, encoding="shift-jis")

        opelist = list(df_s['odpt:operator'])
        for indx in range(len(opelist)):
            if opelist != "":
                opelist[indx]=opelist[indx][0]
        df_s['odpt:operator'] = pd.Series(opelist)

        if self.DEB_FLAG == True:
            df_s.to_csv("search_GPS_near_bus_station_info.csv",encoding='utf_8_sig') #for debug
        return df_s

if __name__ == '__main__':
    test_instance = func_tokyo_public_trans_API()

    #############
    #共通定義API#
    #############

    #カレンダーテーブルの取得
    test_instance.get_Calendar_information()

    #事業者テーブルの取得
    #test_instance.get_Operator_information()


    ###########
    #鉄道用API#
    ###########

    #乗降人数の取得
    #test_instance.get_Train_Passenger_information() #駅すべてについて出力
    #test_instance.get_Train_Passenger_information(operator="odpt.Operator:Keikyu") #京急のみ出力
    #test_instance.get_Train_Passenger_information(station='odpt.Station:Keio.Keio.Chofu') #京王調布駅のみ出力
    #test_instance.get_Train_Passenger_information(railway='odpt.Railway:Tokyu.DenEnToshi')#東急田園都市線のみ出力

    #進行方向の取得
    #test_instance.get_Train_RailDirection_information() #駅すべてについて出力

    #路線情報の取得
    #test_instance.get_Train_Railway_information() #すべての路線について取得
    #test_instance.get_Train_Railway_information(railway_code="odpt.Railway:Toei.Oedo") #都営大江戸線のみについて取得
    #test_instance.get_Train_Railway_information(railway_name="相模原線") #相模原線 のみについて取得
    #test_instance.get_Train_Railway_information(railway_operator="odpt.Operator:JR-West") #JR西の路線のみ取得
    #test_instance.get_Train_Railway_information(railway_LINECODE="R") #みなとみらい線についてのみ取得

    #料金情報の取得
    #test_instance.get_Train_Railway_Fare_information() #すべての路線の料金について取得 (1000駅で打ち切りっぽい?)
    #test_instance.get_Train_Railway_Fare_information(fare_code="odpt.RailwayFare:Tokyu.DenEnToshi.Aobadai.Tokyu.DenEnToshi.Miyamaedaira") #区間コード直接指定　駅コードをくっつけて生成できそう
    #test_instance.get_Train_Railway_Fare_information(operator_name="odpt.Operator:Tokyu") #同一会社内のすべての経路の結果を出力(最大1000)
    #test_instance.get_Train_Railway_Fare_information(from_sation_code="odpt.Station:Toei.Arakawa.ArakawaYuenchimae") #開始駅を指定して同一会社間の経路における料金を出力
    #test_instance.get_Train_Railway_Fare_information(to_sation_code="odpt.Station:Toei.Arakawa.ArakawaYuenchimae") #到着駅を指定して同一会社間の経路における料金を出力

    #駅情報の取得
    #test_instance.get_Train_Railway_Station_information() #すべての路線の料金について取得 (1000駅で打ち切りっぽい?)
    #test_instance.get_Train_Railway_Station_information(station_code="odpt.Station:Tokyu.Oimachi.Ookayama") #大岡山駅の情報を表示（コード指定)
    #test_instance.get_Train_Railway_Station_information(station_name="渋谷")  #渋谷駅の情報を表示 (名称指定) ⇒　運営会社/路線ごとに別レコードとして表示される
    #test_instance.get_Train_Railway_Station_information(operator_code="odpt.Operator:Keikyu")  #京急の駅情報を表示
    #test_instance.get_Train_Railway_Station_information(railway_code="odpt.Railway:TokyoMetro.Chiyoda")  #東京メトロ千代田線の駅情報を表示
    #test_instance.get_Train_Railway_Station_information(station_numcode="DT7")  #駅コード番号による検索　DT7:二子玉川

    #駅時刻表の取得
    #test_instance.get_Train_Railway_StationTimetable_information() #すべての駅の時刻表
    #test_instance.get_Train_Railway_StationTimetable_information(station_code="odpt.Station:Tobu.Nikko.TobuNikko") #東武日光の時刻表(駅名コード)
    #test_instance.get_Train_Railway_StationTimetable_information(station_name="品川") #品川の時刻表(駅名指定 同一名称の駅が複数ある場合は複数出力される)
    #test_instance.get_Train_Railway_StationTimetable_information(operator_code="odpt.Operator:JR-Central") #JR東海の時刻表(運営会社指定)
    #test_instance.get_Train_Railway_StationTimetable_information(railway_code="odpt.Railway:TokyoMetro.Ginza") #東京メトロ銀座線の時刻表(路線コード指定)
    #test_instance.get_Train_Railway_StationTimetable_information(station_numcode="G16") #上野の時刻表(駅番号コード指定G16)

    #列車情報の取得
    #test_instance.get_Train_Railway_Train_information() #すべての列車の運行状況
    #test_instance.get_Train_Railway_Train_information(train_code="odpt.Train:JR-East.Utsunomiya.660M") #列車コードの指定 (JR東　宇都宮線　列車コード660M)
    #test_instance.get_Train_Railway_Train_information(operator_code="odpt.Operator:TokyoMetro") #運営会社コードの指定 (東京メトロ)
    #test_instance.get_Train_Railway_Train_information(railway_code="odpt.Railway:JR-East.Chuo") #路線コードの指定 (JR東日本中央線)

    #列車遅延情報の取得
    #test_instance.get_Train_Railway_Train_Delay_information()   #すべての列車の遅延状況の取得
    #test_instance.get_Train_Railway_Train_Delay_information(traininfo_code="odpt.TrainInformation:JR-East.Yamanote")   #山手線の遅延情報(運行情報コードを指定)
    #test_instance.get_Train_Railway_Train_Delay_information(operator_code="odpt.Operator:Keio")   #京王の運行情報(運行会社コードを指定)
    #test_instance.get_Train_Railway_Train_Delay_information(railway_code="odpt.Railway:Tokyu.TokyuTamagawa")   #東急多摩川線の遅延情報(路線コードを指定)

    #列車時刻表の取得
    #test_instance.get_Train_Railway_TrainTimetable_information()
    #test_instance.get_Train_Railway_TrainTimetable_information(traintimetable_code="odpt.TrainTimetable:Keio.Keio.0067.SaturdayHoliday") #列車タイムスケジュールコード指定 (京王線　0067　土日)
    #test_instance.get_Train_Railway_TrainTimetable_information(trainNumber="ODPT0052") #列車番号指定 (都営浅草線　ODPT0052) ⇒　平日・休日の両方が出力される
    #test_instance.get_Train_Railway_TrainTimetable_information(railway_code="odpt.Railway:TWR.Rinkai") #りんかい線　路線指定 
    #test_instance.get_Train_Railway_TrainTimetable_information(operator_code="odpt.Operator:Toei") #都営　運営会社指定
    #test_instance.get_Train_Railway_TrainTimetable_information(trainType_code="odpt.TrainType:Keio.LimitedExpress") #列車種別 列車タイプコード指定
    #test_instance.get_Train_Railway_TrainTimetable_information(calender="odpt.Calendar:SaturdayHoliday") #土日祝日 カレンダータイプコード指定

    #列車種別情報の取得
    #test_instance.get_Train_Railway_TrainType_information() #すべての列車種別情報の取得
    #test_instance.get_Train_Railway_TrainType_information(traintype_code="odpt.TrainType:Odakyu.LimitedExpress") #小田急特別快速　列車タイプコード指定
    #test_instance.get_Train_Railway_TrainType_information(operator_code="odpt.Operator:Keikyu") #京急　運営会社コード指定



    ###########
    #バス用API#
    ###########

    #バス車両の運行情報の取得
    #test_instance.get_Bus_Bus_CurrentOperation_information() #すべてのバス運行情報の取得
    #test_instance.get_Bus_Bus_CurrentOperation_information(bus_oper_code="odpt.Bus:Toei.Kame21.60001.1.P447") #都営線の亀２１ 東陽町駅前→亀戸駅前 袖ヶ浦　 (運営会社+路線コード+バスID)
    #test_instance.get_Bus_Bus_CurrentOperation_information(busroutePattern_code="odpt.Bus:Toei.Kame21.60001.1.P447") #都営線の亀２１ 東陽町駅前→亀戸駅前 袖ヶ浦　 (運営会社+路線コード+バスID)

    #バス時刻表の取得
    #test_instance.get_Bus_BusTimetable_information() #すべてのバス時刻表の取得
    #test_instance.get_Bus_BusTimetable_information(bus_ttable_code = "odpt.BusTimetable:KokusaiKogyoBus.Aka23.30923001.1.330049.Weekday") #国際工業バス 赤23 平日の時刻表表示(コードで指定)
    #test_instance.get_Bus_BusTimetable_information(operator_code = "odpt.Operator:TokyuBus") #東急バス(運営会社コードで指定)
    #test_instance.get_Bus_BusTimetable_information(busroutePattern_code = "odpt.BusroutePattern:KeioBus.Chou01Ou.360.1") #京王バス　調０１-央線　(運営会社コードで指定)
    #test_instance.get_Bus_BusTimetable_information(bus_routetiltle = "西川62") #西川62　(路線名で指定)
    #test_instance.get_Bus_BusTimetable_information(calender_code = "odpt.Calendar:Holiday") #休日時刻表　(カレンダーコードで指定)

    #バス運行系統情報の取得
    #test_instance.get_Bus_BusroutePattern_information() #すべてのバス運行系統情報の取得
    #test_instance.get_Bus_BusroutePattern_information(bus_routepattern_code="odpt.BusroutePattern:NishiTokyoBus.Ao20.400101.1") #西東京バス　青20
    #test_instance.get_Bus_BusroutePattern_information(operator_code="odpt.Operator:TokyuBus") #東急バス(運営会社コードで指定)
    #test_instance.get_Bus_BusroutePattern_information(route_title="高２３-学") #高２３-学 (路線名で指定)


    #バス運賃情報の取得
    #test_instance.get_Bus_BusroutePatternFare_information() #すべてのバス運行ルートに対する運賃情報の取得
    #test_instance.get_Bus_BusroutePatternFare_information(operator_code="odpt.Operator:JRBusKanto") #JRバス関東　⇒事業者で出るIDと出ないIDがあるような・・・。要確認
    #test_instance.get_Bus_BusroutePatternFare_information(from_pole_code="odpt.BusstopPole:JRBusKanto.Mishimashougakukoumae.36.4") #乗車バス停指定 (同じバス会社内でしか使えなさそう)
    #test_instance.get_Bus_BusroutePatternFare_information(to_pole_code="odpt.Station:Toei.Arakawa.TodenZoshigaya") #降車バス停指定 (同じバス会社内でしか使えなさそう)


    #バス停(標柱)情報の取得
    #test_instance.get_Bus_BusstopPole_information() #すべてのバス停に対する情報の取得
    #test_instance.get_Bus_BusstopPole_information(bus_stoppole_code="odpt.BusstopPole:KeioBus.TamadoubutsukouenEki.752.1") #多摩動物公園前駅　(バス停コード指定)
    #test_instance.get_Bus_BusstopPole_information(bus_stop_name="草津温泉") #草津温泉　(バス停名称指定)
    #test_instance.get_Bus_BusstopPole_information(bus_stop_name="草津温泉") #草津温泉　(バス停名称指定)
    #test_instance.get_Bus_BusstopPole_information(busroutePattern_code="odpt.BusroutePattern:KeioBus.Kuni18.137.1") #京王バス国18 (路線コード指定)
    #test_instance.get_Bus_BusstopPole_information(operator_code="odpt.Operator:OdakyuBus") #小田急バス (運営会社コード指定)


    #バス停(標柱)時刻表情報の取得
    #test_instance.get_Bus_BusstopPoleTimetable_information() #すべてのバス停に対する情報の取得  #EXCELのCSVで見るとなぜか乱れる。長さ?
    #test_instance.get_Bus_BusstopPoleTimetable_information(busstop_timetbl_code="odpt.BusstopPoleTimetable:KeioBus.Yutaka33.Yutaka32.Hodokubogochoume.1302.2.Tamasenta-eki.Weekday") 
    #test_instance.get_Bus_BusstopPoleTimetable_information(bus_stoppole_code="odpt.BusstopPole:KeioBus.Maeharachou.1346.5")  #すべてのバス停に対する情報の取得  #CSVで見るとなぜか乱れる。長さ?
    #test_instance.get_Bus_BusstopPoleTimetable_information(busDirection_code="odpt.BusDirection:TokyuBus.Senzokueki")   #バスの方面 (複数方面が含まれるバス停も表示される)
    #test_instance.get_Bus_BusstopPoleTimetable_information(busroute_code="odpt.Busroute:KeioBus.Tera91")   #バスの路線指定 (複数路線が含まれるバス停も表示される)
    #test_instance.get_Bus_BusstopPoleTimetable_information(operator_code="odpt.Operator:TokyuBus")   #バスの運営会社コード指定
    #test_instance.get_Bus_BusstopPoleTimetable_information(calendar_code="odpt.Calendar:Sunday")   #カレンダーコード指定
    #test_instance.get_Bus_BusstopPoleTimetable_information(date_num="2019-04-01T23:59:43+09:00")   #データ生成日付指定 (どういう使い方を想定しているのか不明・・・)

    #データダンプ用API
    #test_instance.dump_Common_information()    #共通情報のダンプ
    #test_instance.dump_Train_information()     #鉄道情報のダンプ
    #test_instance.dump_Bus_information()       #バス情報のダンプ



    ########################
    ### 地物情報検索 API ###
    ########################

    #GPS座標で近隣に存在する駅の取得
    #test_instance.search_GPS_near_train_station_info(st_lat="35.681236",st_lon="139.767125",radius_m="2000")
    #test_instance.search_GPS_near_train_station_info(st_lat="35.681236",st_lon="139.767125",radius_m="2000",st_name="東京") #駅名を指定した検索

    #GPS座標で近隣に存在するバス停の取得
    #test_instance.search_GPS_near_bus_station_info(st_lat="35.681236",st_lon="139.767125",radius_m="2000")
    test_instance.search_GPS_near_bus_station_info(st_lat="35.681236",st_lon="139.767125",radius_m="2000",st_name="東京駅南口") #駅名を指定した検索



