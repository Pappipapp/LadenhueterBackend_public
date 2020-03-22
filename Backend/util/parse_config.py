import os
import configparser

"""
Keys that shall be searched for in the config keys
"""
key_docker = '_docker'
key_standalone = '_standalone'


def parse_config(path):
    """
    Parses a given config file using the python config parser
    It also applies different transformation to the config to improve the usability in the program

    :param path: path to the config file (should be .cfg)
    :return: parsed config object
    """

    config = configparser.ConfigParser()
    config.read(path)
    config.sections()

    runs_in_docker = os.environ.get('RUNNING_IN_DOCKER_CONTAINER', False)
    for section in config:
        for key in config[section]:
            # Transform values
            value = config[section][key]
            if '\n' in value:
                value = value.split('\n')
                config[section][key] = value

            # Transform keys
            # If run in docker, copy the values of keys like 'port_docker' to key 'port'
            # If run as a standalone, copy the values of keys like 'port_standalone' to key 'port'
            if key.endswith(key_docker) and runs_in_docker:
                config[section][key.replace(key_docker, '')] = value
            elif key.endswith(key_standalone) and not runs_in_docker:
                config[section][key.replace(key_standalone, '')] = value

    return config
