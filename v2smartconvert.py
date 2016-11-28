#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import arrow
from var_utils import start_t, print_time_str, time_str
import sys
from tweet_utils import sentiment_analysis
from telegram import Bot
from modelsnew import Tweets, db_connect, create_db_session, create_tables
import config
import traceback

chat_id = config.tgchat
bot = Bot(token=config.tgtoken)
st = start_t()

db_engine = db_connect()
create_tables(db_engine)
db_session = create_db_session(db_engine)


def main():
    parsed = 1
    rows_inserted = 0
    with open(sys.argv[1]) as f:
        for line in f:

            try:
                doc = json.loads(line)
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                lines = traceback.format_exception(exc_type, exc_value,
                                                   exc_traceback)
                txt = ''.join('' + line for line in lines)
                print(txt)
                bot.sendMessage(chat_id=chat_id, text=str(txt))
                doc = {"limit": {"track": "err"}}

            if doc.get('limit') is None:
                tweet_id = doc.get('id')

                t_published_at = arrow.get(int(doc.get('timestamp_ms')) / 1000
                                           ).format('YYYY-MM-DD HH:mm:ss ZZ')
                t_tweet_text = doc.get('text')
                t_lang = doc.get('lang')
                t_source = doc.get('source',
                                   "").partition('>')[-1].rpartition('<')[0]
                t_mentions = []

                if doc.get('entities').get('user_mentions'):
                    for m in doc.get('entities').get('user_mentions'):
                        t_mentions.append(m.get('screen_name'))

                t_in_reply_to_status_id = doc.get('in_reply_to_status_id')
                t_in_reply_to_user_id = doc.get('in_reply_to_user_id')

                if t_lang == "en":
                    sentiment = sentiment_analysis(doc)
                    if sentiment == "Positive":
                        t_positive = True
                        t_negative = False
                        t_neutral = False
                    elif sentiment == "Negative":
                        t_positive = False
                        t_negative = True
                        t_neutral = False
                    elif sentiment == "Neutral":
                        t_positive = False
                        t_negative = False
                        t_neutral = True
                else:
                    t_positive = None
                    t_negative = None
                    t_neutral = None

                if doc.get("retweeted_status"):
                    t_retweeted = True
                    t_retweeted_id = doc.get("retweeted_status").get('id')
                else:
                    t_retweeted = None
                    t_retweeted_id = None

                if doc.get("quoted_status"):
                    t_quoted = True
                    t_quoted_id = doc.get("quoted_status").get('id')
                else:
                    t_quoted = None
                    t_quoted_id = None

                u_id = doc.get('user').get('id')

                try:
                    u_created_at = arrow.get(doc.get('user').get('created_at'),
                                             "ddd MMM DD HH:mm:ss Z YYYY"
                                             ).format('YYYY-MM-DD HH:mm:ss ZZ')
                except:
                    u_created_at = None
                    bot.sendMessage(chat_id=chat_id, text="date error user")
                u_name = doc.get('user').get('name')
                u_screen_name = doc.get('user').get('screen_name')
                u_description = doc.get('user').get('description')
                u_location = doc.get('user').get('location')
                u_lang = doc.get('user').get('lang')
                u_favourites_count = doc.get('user').get('favourites_count')
                u_followers_count = doc.get('user').get('followers_count')
                u_following_count = doc.get('user').get('friends_count')
                u_statuses_count = doc.get('user').get('statuses_count')
                u_verified = doc.get('user').get('verified')
                u_geo_enabled = doc.get('user').get('geo_enabled')

                keys = {}

                for k in config.keywords:
                    if any(w in line.lower() for w in config.keywords[k]):
                        keys[k] = True

                tweet = Tweets(tweetid=tweet_id,
                               published_at=t_published_at,
                               tweet_text=t_tweet_text,
                               lang=t_lang,
                               source=t_source,
                               mentions=t_mentions,
                               in_reply_to_status_id=t_in_reply_to_status_id,
                               in_reply_to_user_id=t_in_reply_to_user_id,
                               positive=t_positive,
                               negative=t_negative,
                               neutral=t_neutral,
                               retweeted=t_retweeted,
                               retweeted_id=t_retweeted_id,
                               quoted=t_quoted,
                               quoted_id=t_quoted_id,
                               user_id=u_id,
                               created_at=u_created_at,
                               name=u_name,
                               screen_name=u_screen_name,
                               description=u_description,
                               location=u_location,
                               usr_lang=u_lang,
                               favourites_count=u_favourites_count,
                               followers_count=u_followers_count,
                               following_count=u_following_count,
                               statuses_count=u_statuses_count,
                               verified=u_verified,
                               geo_enabled=u_geo_enabled,
                               adidas=keys.get('adidas', False),
                               nike=keys.get('nike', False),
                               barcelona=keys.get('barcelona', False),
                               real=keys.get('realmadrid', False),
                               messi=keys.get('messi', False),
                               ronaldo=keys.get('ronaldo', False))

                db_session.add(tweet)
                rows_inserted += 1

                if not parsed % config.n_commit:
                    db_session.commit()
                    print_time_str(st, parsed, sys.argv[1], rows_inserted)

                if not parsed % config.n_send:
                    try:
                        bot.sendMessage(chat_id=chat_id,
                                        text=time_str(st, parsed, sys.argv[1],
                                                      rows_inserted))
                    except:
                        pass

                parsed += 1

    db_session.commit()

    final = "%s terminated!" % sys.argv[1]
    bot.sendMessage(chat_id=chat_id, text=final)
    bot.sendMessage(chat_id=chat_id, text=time_str(st, parsed, sys.argv[1],
                                                   rows_inserted))

    print_time_str(st, parsed, sys.argv[1], rows_inserted)


if __name__ == '__main__':
    try:
        main()
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines1 = traceback.format_exception(exc_type)
        lines2 = traceback.format_exception(exc_value)
        lines3 = traceback.format_exception(exc_traceback)
        try:
            bot.sendMessage(chat_id=chat_id, text="err on " + sys.argv[1])
            bot.sendMessage(chat_id=chat_id, text=str(lines1))
            bot.sendMessage(chat_id=chat_id, text=str(lines2))
            bot.sendMessage(chat_id=chat_id, text=str(lines3))
        except:
            pass
