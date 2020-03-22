from api import app_api, config
from .error_template import ErrorTemplate

from flask import request, jsonify
from flask_api import status
from flask_cors import cross_origin
from functools import wraps
import datetime
import jwt


"""
Configuration for authorization purposes
"""
authorization_config = config['authorization']


def token_required(f, master=False):
    """
    For a given route, this function ensures that a correct authorization token is provided with the request
    Such a token can be acquired using the '/login' route
    It shall be used as an annotator, i.e. '@token_required'

    :param f: Route to ensure token authorization for
    :param master: If set to True, the decorator tries to decode the token with the master key, if
                    set to False, the decorator tries to decode the token with the secret key
    :return: decorated function
    """

    @wraps(f)
    @cross_origin()
    def decorated(*args, **kwargs):
        """
        Wrapper function to get the token.
        """

        # Extract token from header
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        # Is token missing?
        if not token:
            raise ErrorTemplate('Authorization token is missing!', 401)

        # Check whether the token is valid
        try:
            # In case the route is master-protected
            if master:
                try:
                    jwt.decode(token, authorization_config['master_key'])
                except jwt.DecodeError:
                    raise ErrorTemplate('Authorization token is either invalid or does not possess the necessary'
                                        ' rights to access this route', 401)
            # In case the route is user-protected
            else:
                # Try for user-protection, if that fails, try for master-protection, if that fails, token is invalid
                try:
                    jwt.decode(token, authorization_config['secret_key'])
                except jwt.DecodeError:
                    jwt.decode(token, authorization_config['master_key'])

        except (jwt.DecodeError, jwt.ExpiredSignatureError):

            raise ErrorTemplate('Authorization token is invalid!', 401)

        return f(*args, **kwargs)

    return decorated


@app_api.route('/register', methods=['GET'])
def register():
    """
    This route provides the possibility for a user/master-user to acquire a token, which in return is needed to access
        protected/master-protected routes of the api
    For that, he provides his username as well as the user/master authentication key, which can be set in the
        configuration.
    The returned token is only valid for a given amount of days, which can be set in the configuration file
    """

    # Acquire authorization information
    auth = request.authorization

    # Master case
    if auth and auth.password == authorization_config['master_authorization_key']:
        # Create Token
        token = jwt.encode({'user': auth.username,
                            'exp': datetime.datetime.utcnow() +
                                   datetime.timedelta(days=authorization_config.getint('expiration_days'))},
                           authorization_config['master_key'])

        # Send token to user
        return jsonify({'Token': token.decode('UTF-8')}), status.HTTP_200_OK

    # Invalid Key or missing auth information
    raise ErrorTemplate('Authorization failed', 401)
