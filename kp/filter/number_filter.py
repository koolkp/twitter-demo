# coding=utf-8
# !/usr/bin/env python
# title           :number_filter
# description     :Give a short description about script.
# author          :kp
# date            :4/2/18 4:08 PM
# version         :0.0.1
# notes           :
# python_version  :3.5.2
# ==============================================================================


class NumberFilter(object):

    def __init__(self):
        self.valid_types = ['eq', 'gt', 'gte', 'lt', 'lte']

    def get_filter(self, column, value, filter_type):
        if filter_type is None:
            filter_type = 'eq'
        if filter_type not in self.valid_types:
            return {}
        filter_type = '$' + filter_type
        return {
            column: {
                filter_type: value
            }
        }
