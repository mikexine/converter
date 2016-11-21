#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2
import config

db = config.db

conn = psycopg2.connect(dbname=db.get('database'), user=db.get('user'),
                        host=db.get('host'), password=db.get('password'))
c = conn.cursor()

for k in config.keywords:
    c.execute("DROP TABLE IF EXISTS %s;" % k)

c.execute("DROP TABLE IF EXISTS tweets;")
c.execute("DROP TABLE IF EXISTS trash;")

conn.commit()
conn.close()
