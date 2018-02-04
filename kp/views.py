import json
from _datetime import datetime

from TwitterSearch import *
from bson.json_util import dumps
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from kp.constants import DATE_FORMAT, QUERY_DATE_FORMAT
from kp.data_services import DataService
from kp.export_service import export
from twitter_demo import api_tokens

data_service = DataService()


def search(request):
    response = {}
    if request.method == 'GET':
        try:
            q = request.GET.get('q', None)
            tso = TwitterSearchOrder()  # create a TwitterSearchOrder object
            tso.set_keywords([q])  # let's define all words we would like to have a look for
            tso.set_language('en')  # we want to see German tweets only
            tso.set_include_entities(True)  # and don't give us all those entity information
            tso.set_link_filter()
            # it's about time to create a TwitterSearch object with our secret tokens
            ts = TwitterSearch(
                consumer_key=api_tokens.consumer_key,
                consumer_secret=api_tokens.consumer_secret,
                access_token=api_tokens.access_token,
                access_token_secret=api_tokens.access_token_secret
            )

            # this is where the fun actually starts :)
            i = 0
            for tweet in ts.search_tweets_iterable(tso):
                data = {
                    'text': tweet['text'],
                    'user_name': tweet['user']['name'],
                    'screen_name': tweet['user']['screen_name'],
                    'created_at': datetime.strptime(tweet['created_at'], DATE_FORMAT),
                    'retweet_count': tweet['retweet_count'],
                    'favorite_count': tweet['favorite_count'],
                    'geo': tweet['geo'],
                    'lang': tweet['lang'],
                    'followers_count': tweet['user']['followers_count'],
                    'result_type': tweet['metadata']['result_type'],
                    'user_mentions': [{'name': user['name'], 'screen_name': user['screen_name']} for user in tweet['entities']['user_mentions']],
                    'urls': [{'expanded_url': url['expanded_url'], 'url': url['url'], 'display_url': url['display_url']} for url in tweet[
                        'entities'][
                        'urls']],
                }
                data_service.save(data)
                if i == 100:
                    break
                i += 1

        except TwitterSearchException as e:  # take care of all those ugly errors if there are some
            response["error"] = "%r".format(e)
    else:
        response["error"] = "Search support only GET"
    return HttpResponse(json.dumps(response), content_type='application/json')


@csrf_exempt
def filter(request):
    filter_request = json.loads(request.body.decode('utf-8'))
    response = data_service.get_data(filter_request)
    for data in response:
        data['created_at'] = data['created_at'].strftime(QUERY_DATE_FORMAT)
    return HttpResponse(dumps(response), content_type='application/json')


@csrf_exempt
def export_filter(request):
    filter_request = json.loads(request.body.decode('utf-8'))
    response = data_service.get_data(filter_request)
    for data in response:
        data['created_at'] = data['created_at'].strftime(QUERY_DATE_FORMAT)
        del data['_id']
    export_columns = filter_request.get('export_columns', [])
    return export(response, export_columns)


def metadata(request):
    response = data_service.get_all_metadata()
    return HttpResponse(dumps(response), content_type='application/json')

