from api import app_api

import traceback
from flask import jsonify
from flask_api import status
from flask_cors import cross_origin


class ErrorTemplate(Exception):
    """
    This class is the frame for all exceptions and errors in all routes. For unwanted behaviour
    "raise ErrorTemplate(args)" in the respective routes.
    """

    def __init__(self, warning, status_code=400, payload=None):
        """
        Specifies the exception for its designated purpose

        :param warning: Which warning should be displayed in the JSON output
        :param status_code: Which status_code should accompany the request_answer
        :param payload: optional, additional info that can be shown in the JSON output
        """

        Exception.__init__(self)
        self.warning = warning
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['warning'] = self.warning
        rv['StatusCode'] = self.status_code
        return rv


@app_api.errorhandler(ErrorTemplate)
@cross_origin()
def handle_other_errors(error):
    """
    Registers the ErrorTemplate for the API

    :param error: The error object, that is constructed, when raised in a route
    :return: a response containing a JSON with warning and (optionally) a payload
    """

    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app_api.errorhandler(500)
@cross_origin()
def handle_internal_error(error):
    """
    Registers the general 500 error if any bugs are in the system. Bugs are added to the response-JSON

    :return: A JSON and the specific error, that leads to raising this exception
    """

    print(str(error))
    print(traceback.format_exc())

    response = jsonify({'warning': 'An internal error has occured', 'warning': 'An Error has occurred during your'
                                                                               ' request. Check your request for '
                                                                               'errors. If the problem persists, '
                                                                               'consult the system administrator for '
                                                                               'more details.',
                        'StatusCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                        'StatusDescription': 'InternalServerError'})

    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return response


@app_api.errorhandler(404)
@cross_origin()
def handle_not_found(error):
    """
    Registers the general 404 error, e.g. if wrong URL or unexisting routes are requested.

    :return: A JSON and the specific error, that leads to raising this exception
    """

    print(str(error))

    response = jsonify({'warning': 'Your requested route has not been found',
                        'StatusCode': status.HTTP_404_NOT_FOUND,
                        'StatusDescription': 'NotFound'})

    response.status_code = status.HTTP_404_NOT_FOUND

    return response


@app_api.errorhandler(400)
@cross_origin()
def handle_bad_request(error):
    """
    Registers the general 400 error, e.g. if the JSON in the request is faulty.

    :return: A JSON and the specific error, that leads to raising this exception
    """

    print(str(error))

    response = jsonify({'warning': 'Check the syntax of you request.',
                        'StatusCode': status.HTTP_400_BAD_REQUEST,
                        'StatusDescription': 'BadRequest'})

    response.status_code = status.HTTP_400_BAD_REQUEST

    return response
