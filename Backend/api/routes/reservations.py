from api import app_api, database
from .authorization import token_required

from flask import request, jsonify
import datetime
import uuid


@app_api.route('/reservations', methods=['POST'])
@token_required
def reservations():
    """
    Makes a reservation at a market at a timeslot.
    """

    # Get JSON
    json = request.get_json()

    # Get JSON elements
    user_id = json.get('user_id')
    market_id = json.get('market_id')
    starting_time = json.get('starting_time')

    # Generate a unique reservation ID
    reservation_id = str(uuid.uuid4())

    # Safe the reservation in the respective reservations table in the db
    value = database.make_reservation(user_id,
                                      market_id,
                                      reservation_id,
                                      datetime.datetime.strptime(starting_time, "%Y-%m-%dT%H:%M:%S%z").isoformat())

    # Return the reservation ID
    return jsonify({'reservationID': (value[0])[0]})
