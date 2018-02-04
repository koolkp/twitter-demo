# coding=utf-8
# !/usr/bin/env python
# title           :export_service
# description     :Give a short description about script.
# author          :kp
# date            :4/2/18 10:59 PM
# version         :0.0.1
# notes           :
# python_version  :3.5.2
# ==============================================================================
import json

import pandas
from django.http import HttpResponse


def export(data, columns):
    for _ in data:
        for row in _:
            if isinstance(_[row], list):
                _[row] = json.dumps(_[row])
    df = pandas.read_json(json.dumps(data))
    if len(columns) != 0:
        for column in df.columns:
            if column not in columns:
                del df[column]
    df.to_csv("data.csv", index=False)
    with open("data.csv", 'rb') as file:
        response = HttpResponse(file.read())
    response['Content-Disposition'] = "attachment; filename=data.csv"
    response['mimetype'] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    return response
