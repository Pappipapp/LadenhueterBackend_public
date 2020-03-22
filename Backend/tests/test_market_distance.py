import os
import sys

# NOTE(swenninger): Followed <https://docs.python-guide.org/writing/structure/> for this next line of code
#                   I don't know python...
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from util import market_distance

dist_zero  = market_distance.calculate_distance_in_meters(0,0,0,0)
dist_zero2 = market_distance.calculate_distance_in_meters(30.2,20.1234,30.2,20.1234)
assert dist_zero  == 0.0, '[TEST ERROR] market_distance between equal points should be zero. Got {} instead'.format(dist_zero)
assert dist_zero2 == 0.0, '[TEST ERROR] market_distance between equal points should be zero. Got {} instead'.format(dist_zero2)

dist_random = market_distance.calculate_distance_in_meters(0, 0, 180, 0)
print('[TEST] Dist between (0,0) and (180, 0) should roughly be earth_circumference / 2. Result is ', dist_random)

user_lat  = 48.125
user_long = 11.575

test_markets = [{'id': '5c4006911fdc57eb1e9baedffd1c73be223cddf2bf591f9b9020f43115c675b3',
 'name': 'VollCorner',
 'openingHours':
    {'monday': {'start': '08:00', 'end': '20:00'},
     'tuesday': {'start': '08:00', 'end': '20:00'},
     'wednesday': {'start': '08:00', 'end': '20:00'},
     'thursday': {'start': '08:00', 'end': '20:00'},
     'friday': {'start': '08:00', 'end': '20:00'},
     'saturday': {'start': '08:00', 'end': '20:00'},
     'sunday': {'start': None, 'end': None}},
 'address': 'Lindwurmstraße 80 80337 München',
 'latitude': 48.1257977,
 'longitude': 11.5504061},
 {'id': 'f4aa0f264aef00a73d8dd5a041881039636aaf5b2b9103d3ad731b69222fcfe8',
 'name': 'Edeka',
 'openingHours':
     {'monday': {'start': '07:00', 'end': '20:00'},
     'tuesday': {'start': '07:00', 'end': '20:00'},
     'wednesday': {'start': '07:00', 'end': '20:00'},
     'thursday': {'start': '07:00', 'end': '20:00'},
     'friday': {'start': '07:00', 'end': '20:00'},
     'saturday': {'start': '07:00', 'end': '20:00'},
     'sunday': {'start': None, 'end': None}},
 'address': 'Triftstraße 10 80538 München',
 'latitude': 48.1409523,
 'longitude': 11.5890156},
 {'id': '11b82501d2de9fdbff2ff203e86c07343a6ed73c4cd0717ee4c0d113a0fa2914',
 'name': 'Edeka',
 'openingHours':
     {'monday': {'start': '08:00', 'end': '20:00'},
     'tuesday': {'start': '08:00', 'end': '20:00'},
     'wednesday': {'start': '08:00', 'end': '20:00'},
     'thursday': {'start': '08:00', 'end': '20:00'},
     'friday': {'start': '08:00', 'end': '20:00'},
     'saturday': {'start': '08:00', 'end': '20:00'},
     'sunday': {'start': None, 'end': None}},
 'address': 'Christophstraße 9 80538 München',
 'latitude': 48.1415485,
 'longitude': 11.5852793},
 {'id': '292094c763ca2b6ea6cdd62f9e35ef19a394ed13562b5fb9330dc9465e77a6be',
 'name': 'kleines Kaufhaus im Lehel',
 'openingHours':
    {'monday': {'start': '09:00', 'end': '20:00'},
     'tuesday': {'start': '09:00', 'end': '20:00'},
     'wednesday': {'start': '09:00', 'end': '20:00'},
     'thursday': {'start': '09:00', 'end': '20:00'},
     'friday': {'start': '09:00', 'end': '20:00'},
     'saturday': {'start': None, 'end': None},
     'sunday': {'start': None, 'end': None}},
 'address': 'Triftstraße 2 80538 München',
 'latitude': 48.1398931,
  'longitude': 11.5887094}
]

for market in test_markets:
    dist = market_distance.calculate_distance_in_meters(user_lat, user_long, market['latitude'], market['longitude'])
    market['dist_to_user'] = dist

test_markets.sort(key=lambda market: market['dist_to_user'])

