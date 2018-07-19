from UserService import app
import publicapi


if __name__ == '__main__':
    # Set the logger
    logger = publicapi.setupLogger(publicapi.configRead()['logLevel']['level'], publicapi.configRead()['logLevel']['fileName'])
    # Run the userservice server
    app.run(port=publicapi.configRead()['userservice']['port'], debug=publicapi.configRead()['userservice']['debug'])
    # Connect User db
