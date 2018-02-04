# coding=utf-8
# !/usr/bin/env python
# title           :services
# description     :Give a short description about script.
# author          :kp
# date            :3/2/18 8:39 PM
# version         :0.0.1
# notes           :
# python_version  :3.5.2
# ==============================================================================
from django.conf import settings
from pymongo import MongoClient


class MongoService(object):

    def __init__(self):
        client = MongoClient(settings.MONGO_HOST)
        self.db = client['twitter']

    def save(self, row):
        self.db.tweets.insert_one(row)

    def get_data(self, query, sort_by=None):
        if sort_by is None:
            return list(self.db.tweets.find(query))
        else:
            return list(self.db.tweets.find(query).sort(sort_by))
