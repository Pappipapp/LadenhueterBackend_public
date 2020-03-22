#! /usr/bin/env python3

import json
import os
import sys

# NOTE(swenninger): Followed <https://docs.python-guide.org/writing/structure/> for this next line of code
#                   I don't know python...
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from openstreetapi import openstreetapi

#markets = openstreetapi.get_nearby_markets(48.10, 48.20, 11.55, 11.65)
#print(markets)
#json_string = json.dumps(markets)
#print(json_string)

markets = openstreetapi.get_nearby_markets(48.810072 - 0.05, 48.810072 + 0.05, 9.162132 - 0.05, 9.162132 + 0.05)
#print(markets)
json_string = json.dumps(markets)
print(json_string)

