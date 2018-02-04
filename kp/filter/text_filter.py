# coding=utf-8
# !/usr/bin/env python
# title           :text_filter
# description     :Give a short description about script.
# author          :kp
# date            :4/2/18 4:00 PM
# version         :0.0.1
# notes           :
# python_version  :3.5.2
# ==============================================================================


class TextFilter(object):

    def __init__(self):
        self.valid_types = ['start_with', 'end_with', 'contains', 'equal']

    def get_filter(self, column, value, filter_type):
        if filter_type is None:
            filter_type = 'contains'
        if filter_type not in self.valid_types:
            return {}
        if filter_type == 'start_with' or filter_type == 'equal':
            value = '^' + value
        if filter_type == 'end_with' or filter_type == 'equal':
            value += '$'
        return {
            column: {
                "$regex": value
            }
        }
