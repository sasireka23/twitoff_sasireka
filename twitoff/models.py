from flask_sqlalchemy import SQLAlchemy


# create a DB object

DB =  SQLAlchemy()

class User(DB.Model):
    # id cloumn
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)
    # username column
    username = DB.Column(DB.String, nullable=False)
    # newest tweet id
    newest_tweet_id = DB.Column(DB.BigInteger)

    def __repr__(self):
        return f"User: {self.username}"

class Tweet(DB.Model):
    # id column
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)
    # text column
    text = DB.Column(DB.Unicode(300))
    # store the word embedding of the tweet text, vectorization
    vect =  DB.Column(DB.PickleType, nullable=False)

    # user_id column
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return f"Tweet: {self.text}"

    

