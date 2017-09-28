import os
from flask import Flask


app = Flask(__name__)

if os.environ.get('FLASK_CONFIG'):
    app.config.from_envvar('FLASK_CONFIG')
else:
    app.config.from_object('flask_config_debug')


if __name__ == '__main__':
    # Debugging use only
    app.run(host='0.0.0.0', debug=True, port=8080)
