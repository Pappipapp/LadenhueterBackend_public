from api import app_api, database
from .authorization import token_required
from util.flatten_reservations import flatten_reservations
from openstreetapi.openstreetapi import get_nearby_markets

from flask import request, jsonify
from datetime import datetime


@app_api.route('/get_markets', methods=['POST'])
@token_required
def get_markets():
    """
    Checks for markets in the near proximity. Returns them with the respective market load.
    """

    # Get JSON
    json = request.get_json()

    # Get JSON elements
    user_lat = json.get('latitude')
    user_long = json.get('longitude')

    # Make a bounding box
    user_lat1 = user_lat-0.03
    user_lat2 = user_lat+0.03

    user_long1 = user_long-0.03
    user_long2 = user_long+0.03

    try:
        # Get markets in bounding box from openstreetmap-API
        nearby_markets = get_nearby_markets(user_lat1, user_lat2, user_long1, user_long2)

        # Check every market, if it's already in the db. Otherwise store it there. Check the reservation load of every
        # market and add it to the market. Return every market + load to frontend.
        for i, market in enumerate(nearby_markets):
            database.safe_market(market['id'], market['address'],
                                 market['name'], market['latitude'],
                                 market['longitude'])

            current_date = datetime.now().date()
            reservations = database.get_reservations_for_market(market['id'])
            reservations = flatten_reservations(reservations, current_date)
            nearby_markets[i]['reservations'] = reservations

        return jsonify(nearby_markets)

    # If no market is found
    except ValueError:
        return jsonify({'warning': 'no markets in close proximity'})
