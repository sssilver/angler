import flask
import flask.ext
import yaml
import os

import rod.resources


app = flask.Flask(__name__)
api = flask.ext.restful.Api(app)

rod.resources.register(api)

@app.route('/')
def index():
    return 'Hello'


if __name__ == '__main__':
    # Read the config
    env = os.environ.get('ENV', 'live').lower()
    with open('config/{}.yaml'.format(env)) as config_file:
        config = yaml.safe_load(config_file)

    app.config.update(config['flask'])

    app.run()
