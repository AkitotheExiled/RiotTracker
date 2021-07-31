import pytest
from app import create_app
from app.main.views import *
from app.main.twitter import *


# TEST IF GET_API returns status code 200
# TEST IF get_cp;;ectom tweets returns an empty list
# etc...
@pytest.fixture
def client():
    app = create_app()
    client = app.test_client()
    yield client

@pytest.fixture
def app_context():
    app = create_app()
    client = app.app_context()
    yield client
def test_home_page():
    flask_app = create_app()

    with flask_app.test_client() as tc:
        response = tc.get('/')
        assert response.status_code == 200
        assert b'Riot Charizard' in response.data


def test_convert_twitter_date_datetime():
    #thanks Chris Herring
    timestamp = convert_twitter_date_to_datetime('Fri Oct 09 10:01:41 +0000 2015')
    assert timestamp == '2015-10-09 10:01:41'


def test_read_file():
    assert type(read_file('champs.txt')) == set



def test_get_tweets_from_collection(app_context):
    with app_context:
        collection = '1394767900959928321'
        assert len(get_tweets_from_collection(collection)) == 0

def test_get_api(app_context):
    with app_context:
        get_authed_api()

