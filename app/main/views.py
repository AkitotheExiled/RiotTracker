
from flask import Flask, render_template,request, g, redirect, url_for, current_app, session, jsonify, make_response
from app.main.tasks import run_async_parser, print_msg
from app.main.forms import SearchForm
from . import main
from .database import Tweet, ImageTweet

import json


keywords = ['gameplay', 'preview', 'hotfix', 'deployed', 'servers', 'League', 'PBE', 'abilities', 'VGU', 'balance', 'project', 'adjustments', 'feedback']



@main.before_app_request
def before_request():
    g.search_form = SearchForm()
    g.default_page = 1

@main.route('/')
def index():
    session['default_page'] = g.default_page
    tweets = load_tweets_next_page(1)

    if g.search_form.validate():
        return redirect(url_for('main.search'))
    return render_template('index.html', tweets=tweets.data, default_page=1)

@main.route('/tweets/<int:page>', methods=['GET'])
def load_tweets_next_page(page=1):
    sorted = []
    tweets_per_page = current_app.config['POSTS_PER_PAGE']
    query_offset = page * int(tweets_per_page)
    print(query_offset)
    tweets = Tweet.query.limit(tweets_per_page).offset(query_offset).all()
    for tweet in tweets:
        images = []
        image = ImageTweet.query.filter_by(tweet_id=tweet.id).first()
        if image:
            images.append(image.image)
        sorted.append({'author': tweet.author,
                       'message': tweet.message,
                       'images': images,
                       'link': tweet.perm_link(),
                       'id': tweet.id})
    session['default_page'] += 1
    return make_response(jsonify(sorted, page+1))

@main.route('/process')
def process():
    run_async_parser.delay()

    return 'Request sent to server!'

@main.route('/search')
def search():
    #if not g.search_form.validate():
        #return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    tweets, total = Tweet.search(g.search_form.q.data, page, current_app.config['POSTS_PER_PAGE'])
    #print(tweets)
    #next_url = url_for('main.search', q=g.search.form.q.data, page=page + 1) \
        #if total > page * current_app.config['POSTS_PER_PAGE'] else None
    #prev_url = url_for('main.search', q=g.search.form.q.data, page=page - 1) \
        #if page > 1 else None
    return render_template('search.html', title=('Search'), tweets=tweets)

@main.route('/tweet/<id>')
def view_tweet(id):
    tweet_id = Tweet.get_id_from_perm(perm=id)
    tweet = Tweet.query.filter_by(id=tweet_id).first()
    return render_template('shared_tweet.html', tweet=tweet)

    
    
