from TwitterSearch import *

try:
    tso = TwitterSearchOrder()  # create a TwitterSearchOrder object
    tso.set_keywords(['amitabh'])  # let's define all words we would like to have a look for
    tso.set_language('en')  # we want to see German tweets only
    tso.set_include_entities(False)  # and don't give us all those entity information

    # it's about time to create a TwitterSearch object with our secret tokens
    ts = TwitterSearch(
        consumer_key='ooJylVCH8esrw2RzQIXTEzepR',
        consumer_secret='pEnVbrfRsbJ59PEh6qWhnmxRCJjc2YOm9wIlb9uxZoGPptsSew',
        access_token='181187891-Axx9o1WKBJGx8FChmMatH2yf4ydMPYu8m6WaPCYF',
        access_token_secret='xJGcHlFyvnFHFUg4kUiEignpH6teV8oZcweKa23xF9VQP'
    )

    # this is where the fun actually starts :)
    for tweet in ts.search_tweets_iterable(tso):
        print('@%s tweeted: %s' % (tweet['user']['screen_name'], tweet['text']))

except TwitterSearchException as e:  # take care of all those ugly errors if there are some
    print(e)
