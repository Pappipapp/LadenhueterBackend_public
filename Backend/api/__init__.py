from util.parse_config import parse_config
from flask_api import FlaskAPI

"""
Initializes the API application and makes it available for the whole package
"""
app_api = FlaskAPI(
    __name__)

"""
Holds an instance of APIDatabase and makes it available for the whole package
"""
database = None


"""
Version of the backend system
It is set via start_api()
"""
version = None

"""
Read the configuration and make it available for the package
"""
config = parse_config('./api/config.cfg')


def start_api(production=False, version_val='0.0.0'):
    """
    Starts the flask api
    Only start the api through this interface in order to ensure a correct initialization

    :param production: Tells the system, if the api should either be started in development or production mode
                            Development mode may never be used when the product is deployed!
    :param version_val: Version of the anonymization system
    """

    print('Starting api...')
    global app_api

    # Set version
    global version
    version = version_val

    # Initialize Key for authorization
    app_api.config['SECRET_KEY'] = config['authorization']['secret_key']

    # Ensure proper encoding of JSONs
    app_api.config['JSON_AS_ASCII'] = False

    # Import database here to prevent circular imports
    from database.api_database import APIDatabase

    # Start database
    with APIDatabase() as db:
        global database
        database = db

        # Initialize routes
        import api.routes.routes
        # Get host and port
        host = config['general']['host']
        port = config['general'].getint('port')

        if production:
            print('Api is serving on https://{}:{} in development mode'.format(host, port))
            app_api.run(debug=False, host=host, port=port, ssl_context=None)

        # dont ask
        else:
            print('Api is serving on https://{}:{} in development mode'.format(host, port))
            app_api.run(debug=False, host=host, port=port, ssl_context=None)