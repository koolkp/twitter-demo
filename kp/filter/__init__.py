# coding=utf-8
# !/usr/bin/env python
# title           :__init__.py
# description     :Give a short description about script.
# author          :kp
# date            :4/2/18 3:59 PM
# version         :0.0.1
# notes           :
# python_version  :3.5.2
# ==============================================================================
from kp.filter.number_filter import NumberFilter
from kp.filter.range_filter import RangeFilter
from kp.filter.text_filter import TextFilter


class Filter(object):

    def __init__(self):
        self.text_filters = ['text', 'user_name', 'screen_name', 'lang', 'user_mentions.name', 'user_mentions.screen_name', 'urls.url',
                             'urls.expanded_url', 'urls.display_url']
        self.number_filters = ['retweet_count', 'favorite_count', 'followers_count']
        self.date_range_filters = ['created_at']
        self.text_filter_obj = TextFilter()
        self.number_filter_obj = NumberFilter()
        self.date_range_filter_obj = RangeFilter()
        self.query = {}

    def get_filter(self, column, value, filter_type):
        if column in self.text_filters:
            return self.text_filter_obj.get_filter(column, value, filter_type)
        if column in self.number_filters:
            return self.number_filter_obj.get_filter(column, value, filter_type)
        if column in self.date_range_filters:
            return self.date_range_filter_obj.get_filter(column, value, filter_type)
