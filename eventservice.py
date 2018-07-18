from EventService import app
import logging
import os.path
import yaml
import sys


def configRead():

    if os.path.isfile('config.yaml'):
        with open('config.yaml', 'r') as f:
            doc = yaml.load(f)
        config = {'datastore': doc['datastore'], 'eventservice': doc['eventservice'], 'logLevel': doc['logLevel']}
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
    # Run the eventservice server
    app.run(port=configRead()['eventservice']['port'], debug=configRead()['eventservice']['debug'])
    # Connect event db
