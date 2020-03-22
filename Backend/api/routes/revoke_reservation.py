from api import app_api, database
from .authorization import token_required

from flask import request, jsonify


@app_api.route('/revoke_reservations', methods=['POST'])
@token_required
def revoke_reservations():
    """
    Revoke the reservation at

    :param reservation_id: ID of the reservation to be revoked
    """

    # Get JSON
    json = request.get_json()

    # Get JSON elements
    reservation_id = json.get('reservation_id')

    # Safe the reservation in the respective reservations table in the db
    value = database.revoke_reservation(reservation_id)

    # Return the reservation ID
    if len(value) == 1:
        return jsonify({'status': 'Reservation was revoked at {}'.format(value)})
    else:
        return jsonify({'status': 'No reservation was found at {}'.format(reservation_id)})
