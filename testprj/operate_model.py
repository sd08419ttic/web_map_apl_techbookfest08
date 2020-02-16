#!/usr/bin/env python
# -*- coding: utf-8 -*-
#2章　データベースの管理 データを操作する(スクリプトからのデータベース操作)
import os
import django

#下記行はmanage.pyからコピーする (プロジェクト名によって異なる)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testprj.settings')
django.setup()
from testapp.models import Station_MODEL    #modelsに記述したクラス名に合わせる

#テーブルの作成
def create_table(target_dataid,target_name,target_latitude,target_longitude):
    Station_MODEL.objects.create(dataid=target_dataid,name=target_name,latitude=target_latitude, longitude=target_longitude)

#データの検索と取得 (単一データ)
def read_table_ID(target_dataid):
    #同一IDが複数存在すると例外発生するので注意
    chk_tmp = Station_MODEL.objects.get(dataid=target_dataid)
    print(chk_tmp.dataid,chk_tmp.name,chk_tmp.latitude,chk_tmp.longitude)
    return

#データの検索と取得 (複数ファイル)
def filter_table_ID(target_name):
    #検索条件に当てはまる複数のデータを取得する場合
    chk_tmp = Station_MODEL.objects.filter(name__contains=target_name)
    #上記は名前に指定した文字列を含んでいるかを判定
    #その他にも様々な条件を検索できる(大小や単語検索など。下記公式URLを参照)
    #https://docs.djangoproject.com/en/3.0/ref/models/querysets/
    for indx in range(len(chk_tmp)):
        print(chk_tmp[indx].dataid,chk_tmp[indx].name,chk_tmp[indx].latitude,chk_tmp[indx].longitude)
    return

#データの更新(csvファイルから一括取得)
def update_table(target_dataid,target_name,target_latitude,target_longitude):
    #一度データを検索し、該当があれば更新、なければ新規作成
    chk_tmp = Station_MODEL.objects.update_or_create(dataid=target_dataid,
            defaults={'name':target_name,'latitude':target_latitude, 'longitude':target_longitude})

#データの削除（指定したID)
def remove_table(target_dataid):
    #一度データを検索し、該当がある場合のみ削除
    chk_tmp = Station_MODEL.objects.get(dataid=target_dataid)
    chk_tmp.delete()

#データの全件削除（指定したID)
def clear_DB_ALL():
    #一度データを検索し、該当がある場合のみ削除
    Station_MODEL.objects.all().delete()


if __name__ == '__main__':
    #DBに登録してある全ての情報を削除
    clear_DB_ALL()
    #DBへの登録
    create_table(1,"新橋駅",35.666415, 139.758693)
    create_table(2,"八丁堀",35.674620, 139.776878)
    create_table(3,"浜松町駅",35.655392, 139.757132)
    create_table(4,"虎ノ門駅",35.670134, 139.750073)
    create_table(5,"桜田門駅",35.677324, 139.751377)
    #DBから特定のIDの情報を取得
    print("ID検索 (対応するデータが1つのみ)")
    read_table_ID(1)
    #DBから条件に当てはまるものを取得
    print("条件検索 (複数のデータを取得)")
    filter_table_ID("門")
    #データの更新(ID指定してなければ新規データ登録)
    print("データの更新")
    update_table(3,"水道橋駅",35.702044, 139.753405)
    update_table(6,"飯田橋駅",35.702084, 139.745025)
    #データの削除(ID指定)
    remove_table(2)
    print("finished!!")
