import json

from app import create_app, db
from app.main.database import User, Tweet, ImageTweet

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return dict(db=db,User=User, Tweet=Tweet, ImageTweet=ImageTweet)
