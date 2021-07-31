from os import path
from contextlib import contextmanager
from sqlalchemy.ext.declarative import declarative_base
import pytest
from app import create_app, db
from app.main.database import User, Tweet, ImageTweet
import datetime



Base = declarative_base()

@contextmanager
def not_raises(exception):
    try:
        yield
    except exception:
        raise pytest.fail(f"DID RAISE {exception}")

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()

    testing_client = flask_app.test_client()

    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()

@pytest.fixture(scope='module')
def init_database():

    db.create_all()
    user1 = User(username='RiotAugust')
    tweet1 = Tweet(message='Taking a break from League today to play Loop Hero.',author_id=user1.id)

    db.session.add(user1)
    db.session.add(tweet1)
    db.session.commit()

    yield db

    db.drop_all()

def test_new_user():
    """
    GIVEN a user model
    WHEN a new User is created
    THEN check the username
    """
    new_user = User(username='RiotIke')
    assert new_user.username == 'RiotIke'

def test_new_tweet():
    """
    GIVEN a tweet model
    WHEN a new Tweet is created
    THEN check the message, is_dmca, created_at
    :return:
    """
    new_tweet = Tweet(message='Neeko new skin is out!', is_dmca=False)
    assert new_tweet.message == 'Neeko new skin is out!'
    assert new_tweet.is_dmca is False

def test_new_image():
    """
    GIVEN an Image model
    WHEN a new Image is created
    THEN check the image
    :return:
    """
    new_image = ImageTweet(image='/static/exampleimage.png')
    assert new_image.image == '/static/exampleimage.png'

