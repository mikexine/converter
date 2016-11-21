# token and chat id for telegram, just for notification purposes
tgtoken = ""
tgchat = ""

# connection data for the database
db = {
    "database": "",
    "user": "",
    "host": "",
    "port": 5432,
    "password": ""
}

# generating sqlalchemy db url
DB_URL = "postgresql://%s:%s@%s:%s/%s" % (
         db.get('user'), db.get('password'),
         db.get('host'), db.get('port'), db.get('database'))

# dict with "name_of_set": [array_of_related_keywords]
keywords = {
    "set1": ["keyword1", "keyword2"],
    "set2": ["keyword1", "keyword2", "keyword3", "keyword4"],
    "set3": ["keyword1", "keyword2", "keyword3"]
}

# define how often data are committed
n_commit = 123

# define how often notifications are sent
n_send = 123
