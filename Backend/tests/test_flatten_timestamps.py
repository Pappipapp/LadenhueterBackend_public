#! /usr/bin/env python3

import json
import os
import sys

# NOTE(swenninger): Followed <https://docs.python-guide.org/writing/structure/> for this next line of code
#                   I don't know python...
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from util.flatten_reservations import flatten_reservations

"2020-03-22T00:00:00+0000"
"2020-03-22T00:30:00+0000"
"2020-03-22T14:00:00+0000"
"2020-03-22T14:30:00+0000"
"2020-03-22T14:00:00+0000"
"2020-03-22T14:00:00+0000"
"2020-03-22T24:30:00+0000"


test_timeslots = [
    ["2020-03-22T00:00:00+0000"],
    ["2020-03-22T00:30:00+0000"],
    ["2020-03-22T14:00:00+0000"],
    ["2020-03-22T14:30:00+0000"],
    ["2020-03-22T14:00:00+0000"],
    ["2020-03-22T14:00:00+0000"],
    ["2020-03-22T24:30:00+0000"], # bogus timestamp to test error handling
]

# Manual solution
histogram_should_be = [
    1, 1,  # 00:00, 00:30
    0, 0,  # 01:00, 01:30
    0, 0,  # 02:00, 02:30
    0, 0,  # 03:00, 03:30
    0, 0,  # 04:00, 04:30
    0, 0,  # 05:00, 05:30
    0, 0,  # 06:00, 06:30
    0, 0,  # 07:00, 07:30
    0, 0,  # 08:00, 08:30
    0, 0,  # 09:00, 09:30
    0, 0,  # 10:00, 10:30
    0, 0,  # 11:00, 11:30
    0, 0,  # 12:00, 12:30
    0, 0,  # 13:00, 13:30
    3, 1,  # 14:00, 14:30
    0, 0,  # 15:00, 15:30
    0, 0,  # 16:00, 16:30
    0, 0,  # 17:00, 17:30
    0, 0,  # 18:00, 18:30
    0, 0,  # 19:00, 19:30
    0, 0,  # 20:00, 20:30
    0, 0,  # 21:00, 21:30
    0, 0,  # 22:00, 22:30
    0, 0,  # 23:00, 23:30
]

histogram = flatten_reservations(test_timeslots)

assert histogram == histogram_should_be, '[TEST ERROR] Histograms do not match:\n{}\n  vs.\n{}'.format(histogram, histogram_should_be)
