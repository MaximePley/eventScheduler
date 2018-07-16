from UserService import app
import logging
import os.path
import yaml
import sys


def configRead():

    if os.path.isfile('config.yaml'):
        with open('config.yaml', 'r') as f:
            doc = yaml.load(f)
        config = {'datastore': doc['datastore'], 'userservice': doc['userservice'], 'logLevel': doc['logLevel']}
        return config
    else:
        sys.exit('No config file')


def setupLogger(logLevel='INFO', filename='execution.log'):

    logging.basicConfig(filename=filename, format='%(asctime)s, %(message)s')
    logging.getLogger().setLevel(logLevel)
    return setupLogger


if __name__ == '__main__':
    # Read the config
    config = configRead()
    # Set the logger
    logger = setupLogger(configRead()['logLevel']['level'], configRead()['logLevel']['fileName'])
    # Run the userservice server
    app.run(port=configRead()['userservice']['port'], debug=configRead()['userservice']['debug'])
    # Connect User db
