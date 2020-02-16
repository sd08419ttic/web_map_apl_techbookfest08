# -*- coding: utf-8 -*-
from django import forms
from testapp.models import Station_MODEL

class Custom_form (forms.Form):
    station_label = forms.ModelChoiceField(
        label='test',   #ラベル名を設定したい場合
        queryset=Station_MODEL.objects.all(),   #全てのデータを表示
        widget=forms.Select,    #Select Boxを表示
        to_field_name='name',   #表示対象とする
        required=False, #選択を必須としない
    )





