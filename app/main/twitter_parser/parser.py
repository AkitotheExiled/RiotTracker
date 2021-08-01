from app import db
from app.main.twitter.auth import get_authed_api
from app.main.database import User, Tweet, ImageTweet
from datetime import datetime
from sqlalchemy.exc import NoResultFound
from definitions import ROOT_DIR

import requests
import shutil
import tweepy
import os
COLLECTIONS = ['1365181916622716937', '1365182909980676102', '1365182240087371776', '1365182654488793088', \
               '1368077727677345794']



def convert_twitter_date_to_datetime(timestamp):
    if type(timestamp) != type(''):
        return timestamp
    return datetime.strftime(datetime.strptime(str(timestamp), '%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S')

def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance



def get_instance(model, **kwargs):
    try:
        return db.session.query(model).filter_by(**kwargs).first()
    except NoResultFound:
        return

def insert_tweets_into_database(tweets):
    for tweet in tweets:
        new_user = get_or_create(db.session,model=User,username=tweet['user'].lower())

        new_tweet = get_or_create(db.session,model=Tweet,message=tweet['text'], created_at=tweet['created_at'], author=new_user.username)
        for image in tweet['images']:
            get_or_create(db.session,model=ImageTweet,image=image, tweet_id=new_tweet.id)

def get_tweets_from_collection(collection_id):
    path = os.path.join(ROOT_DIR, 'app/static/images')
    api = get_authed_api()
    tweets = []
    for tweet in tweepy.Cursor(api.list_timeline, list_id=collection_id, include_rts=False, include_entities=True,
                               tweet_mode="extended").items():
        if tweet is None:
            break
        images = []
        text = None
        if 'media' in tweet.entities:
            for image in tweet.entities['media']:
                save_path = r'C:'
                image_path = image['media_url'].split("/")[-1]
                save_image(image['media_url'], path)
                images.append(image_path)
        try:
            if tweet.retweeted_status:
                text = tweet.retweeted_status.full_text
        except AttributeError:
            text = tweet.full_text
        saved_tweet = {'user': tweet.user.screen_name,
                       'text': text,
                       'tags': set(),
                       'images': images,
                       'created_at': convert_twitter_date_to_datetime(tweet.created_at)}
        tweets.append(saved_tweet)
    return tweets


def save_image(url, destination):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        image_path = url.split("/")[-1]
        with open(os.path.join(destination,image_path), 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
        f.close()

def get_recent_tweets():
    return get_tweets_from_collection(1368077727677345794)

def write_file(text):
    with open('tweets.json', 'a+', encoding="utf-8") as f:
        f.write(text)
    f.close()

def read_file(filename):
    with open(filename) as f:
        output = f.read().split(',')
    #return set(output)
    return output

def sort_tweets(tweets):
    tweets.sort(key= lambda tweet: tweet['created_at'])

def league_related(body):
    body = body.lower()
    #body_set = set(body.split(" "))
    keywords = read_file('keywords.txt')
    #if body_set.intersection(champions):
        #return True
    #return False
    for keyword in keywords:
        if keyword in body:
            return True
    return False

def is_league_related(tweets):
    index = 0
    for tweet in tweets:
        if not league_related(tweet['text']):
            tweets.pop(index)
        index +=1
    return tweets

def process_tweets(tweets):
    league_related_tweets = is_league_related(tweets)
    #tag_n_sorted_tweets = sort_tweets(tagged_tweets)
    insert_tweets_into_database(league_related_tweets)
    print("Processed tweets.")


def get_tweets_from_all_collections():
    for collection_id in COLLECTIONS:
        tweets = get_tweets_from_collection(collection_id)
        process_tweets(tweets)



def run_parser():
    get_tweets_from_all_collections()
    print("running")

if __name__ == "__main__":
    run_parser()