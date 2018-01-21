import json

from TwitterSearch import *
from django.http import HttpResponse

from twitter_demo import api_tokens


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
                response[tweet['user']['screen_name']] = tweet['text']
                if i == 100:
                    break
                i += 1

        except TwitterSearchException as e:  # take care of all those ugly errors if there are some
            response["error"] = "%r".format(e)
    else:
        response["error"] = "Search support only POST"
    return HttpResponse(json.dumps(response), content_type='application/json')
