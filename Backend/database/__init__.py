from util.parse_config import parse_config

import psycopg2

"""
Define the errros that db-interfaces may throw.
Usage-Example: except db_errors_to_catch as e
"""
db_errors_to_catch = (psycopg2.Error, ValueError)

"""
Read the configuration and make it available for the package
"""
config = parse_config('./database/config.cfg')
