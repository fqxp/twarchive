#! /usr/bin/env python3
import tweepy
import json
import logging


def setup_logging():
    logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(name)s [%(levelname)s]: %(message)s')
    logging.getLogger('requests').setLevel(logging.CRITICAL)
    logging.getLogger('requests_oauthlib').setLevel(logging.CRITICAL)
    logging.getLogger('oauthlib').setLevel(logging.CRITICAL)
    logging.getLogger('urllib3').setLevel(logging.CRITICAL)
    logging.getLogger('tweepy').setLevel(logging.CRITICAL)


def read_twitter_credentials(filename):
    with open(filename, 'r') as fp:
        return json.load(fp)


class TwitterApi:
    def __init__(self, auth_data):
        self._api = self.authenticate(auth_data)

    def authenticate(self, auth_data):
        auth = tweepy.OAuthHandler(
                auth_data['consumer_key'],
                auth_data['consumer_secret'])
        auth.set_access_token(
                auth_data['access_token'],
                auth_data['access_token_secret'])
        return tweepy.API(auth, wait_on_rate_limit_notify=True)

    def get_user_id(self, screen_name):
        user_info = self._api.get_user(screen_name)
        return user_info.id

    def search(self, query):
        return self._api.search(query, rpp=100)


if __name__ == '__main__':
    twitter_credentials = read_twitter_credentials('./config.json')
    api = TwitterApi(TWITTER_CREDENTIALS)

    import pprint
    for result in api.search('#G20HH17'):
        pprint.pprint(result)
