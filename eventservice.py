from EventService import app
import publicapi


if __name__ == '__main__':
    # Set the logger
    logger = publicapi.setupLogger(publicapi.configRead()['logLevel']['level'], publicapi.configRead()['logLevel']['fileName'])
    # Run the eventservice server
    app.run(port=publicapi.configRead()['eventservice']['port'], debug=publicapi.configRead()['eventservice']['debug'])
    # Connect event db
