from app import db
import datetime
from itsdangerous.url_safe import URLSafeSerializer
import os
from search import add_to_index, remove_from_index, query_index


class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)

db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    tweets = db.relationship("Tweet")

class ImageTweet(db.Model):
    __tablename__ = 'imagetweet'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.Text)
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweet.id'))
    
class Tweet(SearchableMixin, db.Model):
    __tablename__ = 'tweet'
    __searchable__ = ['message', 'author']
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    is_dmca = db.Column(db.Boolean, default=False)
    images_id = db.relationship("ImageTweet")
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    author = db.Column(db.String(64), db.ForeignKey('user.username'))

    def perm_link(self):
        key = os.environ.get("secret_key") or "secret-key"
        serializer = URLSafeSerializer(key, salt="tweetforsalt")
        return serializer.dumps(self.id)

    def get_id_from_perm(perm):
        key = os.environ.get("secret_key") or "secret-key"
        serializer = URLSafeSerializer(key, salt="tweetforsalt")
        return serializer.loads(perm)

