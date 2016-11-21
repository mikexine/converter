from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import config

DeclarativeBase = declarative_base()


def db_connect():
    return create_engine(config.DB_URL)


def create_db_session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def create_tables(engine):
    for k in config.keywords:
        globals()[k] = type(k, (DeclarativeBase, Users,), {'__tablename__': k})
    globals()["trash"] = type("trash", (DeclarativeBase, Users,),
                              {'__tablename__': "trash"})
    DeclarativeBase.metadata.create_all(engine)


class Tweets(DeclarativeBase):
    __tablename__ = "tweets"

    id = Column(BigInteger, primary_key=True)
    published_at = Column('published_at', DateTime)
    tweet_text = Column('tweet_text', String)
    lang = Column('lang', String)
    source = Column('source', String, nullable=True)
    mentions = Column('mentions', String, nullable=True)
    in_reply_to_status_id = Column('in_reply_to_status_id',
                                   BigInteger, nullable=True)
    in_reply_to_user_id = Column('in_reply_to_user_id',
                                 BigInteger, nullable=True)
    positive = Column('positive', Boolean, nullable=True)
    negative = Column('negative', Boolean, nullable=True)
    neutral = Column('neutral', Boolean, nullable=True)
    retweeted = Column('retweeted', Boolean, nullable=True)
    retweeted_id = Column('retweeted_id', BigInteger, nullable=True)
    quoted = Column('quoted', Boolean, nullable=True)
    quoted_id = Column('quoted_id', BigInteger, nullable=True)
    user_id = Column('user_id', BigInteger)


class Users():
    # id = Column(Integer, primary_key=True)
    userid = Column(BigInteger, primary_key=True)
    created_at = Column('created_at', DateTime)
    name = Column('name', String)
    screen_name = Column('screen_name', String)
    description = Column('description', String, nullable=True)
    location = Column('location', String, nullable=True)
    lang = Column('lang', String, nullable=True)

    favourites_count = Column('favourites_count', BigInteger, nullable=True)
    followers_count = Column('followers_count', BigInteger, nullable=True)
    following_count = Column('following_count', BigInteger, nullable=True)
    statuses_count = Column('statuses_count', BigInteger, nullable=True)

    verified = Column('verified', Boolean, nullable=True)
    geo_enabled = Column('geo_enabled', Boolean, nullable=True)
