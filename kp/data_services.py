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
from datetime import datetime

from kp.constants import QUERY_DATE_FORMAT
from kp.filter import Filter
from kp.mongo_services import MongoService


class DataService(object):

    def __init__(self):
        self.mongo_client = MongoService()
        self.filter_client = Filter()

    def get_query(self, filters):
        query = []
        for column_filter in filters:
            column = column_filter['column']
            partial_q = []
            if column == 'user_mentions':
                column_name = 'user_mentions.name'
                column_screen_name = 'user_mentions.screen_name'
                pq = self.filter_client.get_filter(column_name, column_filter['value'], column_filter['filter_type'])
                partial_q.append(pq)
                pq = self.filter_client.get_filter(column_screen_name, column_filter['value'], column_filter['filter_type'])
                partial_q.append(pq)
                q = {'$or': partial_q}
            elif column == 'urls':
                column_url = 'urls.url'
                column_expanded_url = 'urls.expanded_url'
                column_display_url = 'urls.display_url'
                pq = self.filter_client.get_filter(column_url, column_filter['value'], column_filter['filter_type'])
                partial_q.append(pq)
                pq = self.filter_client.get_filter(column_expanded_url, column_filter['value'], column_filter['filter_type'])
                partial_q.append(pq)
                pq = self.filter_client.get_filter(column_display_url, column_filter['value'], column_filter['filter_type'])
                partial_q.append(pq)
                q = {'$or': partial_q}
            elif column == 'created_at':
                value = column_filter['value']
                value[0] = datetime.strptime(value[0], QUERY_DATE_FORMAT)
                value[1] = datetime.strptime(value[1], QUERY_DATE_FORMAT)
                column_filter['value'] = value
                q = self.filter_client.get_filter(column_filter['column'], value, column_filter.get('filter_type', None))
            else:
                q = self.filter_client.get_filter(column_filter['column'], column_filter['value'], column_filter.get('filter_type', None))
            query.append(q)
        return {'$and': query}

    def get_data(self, request):
        query = self.get_query(request.get('filters', []))
        sort_by = request.get('sort_by', None)
        sort_by_list = []
        if sort_by is not None:
            for sort_by_column in sort_by:
                sort_by_list.append((sort_by_column['column'], sort_by_column['order']))
        return self.mongo_client.get_data(query, sort_by_list)

    def save(self, row):
        self.mongo_client.save(row)

    def get_all_metadata(self):
        response = []
        for column in self.filter_client.text_filters:
            text_filter = {
                "column": column,
                "filter_type": self.filter_client.text_filter_obj.valid_types
            }
            response.append(text_filter)
        for column in self.filter_client.number_filters:
            text_filter = {
                "column": column,
                "filter_type": self.filter_client.number_filter_obj.valid_types
            }
            response.append(text_filter)
        for column in self.filter_client.date_range_filters:
            text_filter = {
                "column": column,
                "filter_type": [QUERY_DATE_FORMAT, QUERY_DATE_FORMAT]
            }
            response.append(text_filter)
        return response
