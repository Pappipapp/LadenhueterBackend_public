from api import start_api
from util.parse_config import parse_config

if __name__ == '__main__':

    # Load Configuration
    config = parse_config('./config.cfg')

    # Get required fields
    version = config['general'].get('version', '0.0.0')
    is_production = config['general'].getboolean('production')

    # Start API
    start_api(is_production, version)
