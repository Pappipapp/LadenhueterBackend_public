from api import app_api
from flask import jsonify
from flask_api import status


@app_api.route('/test', methods=['GET'])
def test():
    """
    For testing purposes. Checks if backend is alive.
    """

    return jsonify({'test': "hi"}), status.HTTP_200_OK
