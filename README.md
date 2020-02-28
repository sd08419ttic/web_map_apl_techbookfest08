# 技術書典8 Django/Leaﬂet/Herokuで作るWeb地図アプリ開発超入門サポートページ

本サイトでは技術書典8で販売した『Django/Leaﬂet/Herokuで作るWeb地図アプリ開発超入門』のサンプルスクリプト
を公開しています。

# 動作環境

* Anaconda3 (Python3.7)
* PostgreSQL (9.6.15)
* OSGeo4W (3.0.2)

# Pythonライブラリ

pip install django ==2.2.7

pip install django - leaflet ==0.25.0

pip install django - geojson ==2.12.0

pip install django - sslserver ==0.21

pip install django -cors - headers ==3.2.0

pip install psycopg2 ==2.8.4

conda install -c conda - forge gdal

pip install jsonfield ==2.0.2

pip install pyproj ==2.4.1

pip install django - heroku ==0.3.1

東京公共交通APIに関するAPIはtokenが必要となるので動作させるためには下記ページで取得後に
open_data_web_apiのself.consumerKeyを書き換えてください。

# 本書/コードに関する連絡先

不明点などがあれば本githubのissuesに記載してご連絡ください。
もしくは下記メールアドレスにご連絡いただいてもかまいません。

i35447take@gmail.com


