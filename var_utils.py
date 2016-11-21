#!/usr/bin/env python
# -*- coding: utf-8 -*-

# assess gender??
# include coordinates

# retweeted_status
# add retweeted (yes/no)
# add retweeted_id (1092401823)

# quoted_status
# add quoted (yes/no)
# add quoted_id

import time
import datetime

rows = [6409921, 5310611]


def start_t():
    return time.time()


def secs_to_HMS(secs):
    if secs < 3600:
        return datetime.datetime.fromtimestamp(secs).strftime('%M:%S')
    else:
        return datetime.datetime.fromtimestamp(secs).strftime('%H:%M:%S')


def time_str(start_time, a, ind, rows_inserted):
    runtime = (time.time() - start_time)

    headline = "--- file: %s ---" % ind
    if "1" in ind:
        i = 0
    else:
        i = 1

    expected_missing_time = (runtime * (rows[i] - a)) / a
    expected_total_time = (runtime * rows[i]) / a

    parsed_str = "--- %s lines parsed, ~%s to go ---" % (a, (rows[i] - a))
    inserted_str = "--- %s rows inserted ---" % rows_inserted
    runtime_str = "--- script running since %s seconds ---" % runtime
    estimation_str = "--- %s hh:mm:ss expected time to end ---" % \
                     secs_to_HMS(expected_missing_time)
    estimation_total_str = "--- %s hh:mm:ss tot expected running time ---" % \
                           secs_to_HMS(expected_total_time)

    txt = "%s\n%s\n%s\n%s\n%s\n%s" % (headline, parsed_str, inserted_str,
                                      runtime_str, estimation_str,
                                      estimation_total_str)
    return txt


def print_time_str(start_time, a, ind, rows_inserted):
    print(time_str(start_time, a, ind, rows_inserted))
