# coding=utf-8
# !/usr/bin/env python
# title           :range_filter
# description     :Give a short description about script.
# author          :kp
# date            :4/2/18 4:04 PM
# version         :0.0.1
# notes           :
# python_version  :3.5.2
# ==============================================================================


class RangeFilter(object):

    def __init__(self):
        pass

    def __get_filter(self, column, value):
        start_index = value[0]
        end_index = value[1]
        if start_index > end_index:
            return {}
        return {column: {'$gte': start_index, '$lt': end_index}}

    def get_filter(self, column, value, filter_type=None):
        return self.__get_filter(column, value)
