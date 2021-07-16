import tweepy
from tweepy.parsers import JSONParser
from flask import current_app
def get_authed_api():
    auth = tweepy.OAuthHandler(current_app.config['TWIT_API_KEY'], current_app.config['TWIT_API_SECRET'])
    auth.set_access_token(current_app.config['TWIT_API_TOKEN'], current_app.config['TWIT_API_SECRET_TOKEN'])

    api = tweepy.API(auth)
    return api