import os
import logging
import yaml
import locale

import rod


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('rod')


def main():
    # Parse the config
    try:
        env = os.environ.get('ENV', 'live')

        with open('config/{}.yaml'.format(env)) as config_file:
            config = yaml.load(config_file)

        log.info('Starting Angler.Rod/{env} on {host}:{port}'.format(
            env=env,
            host='localhost',
            port=config['network']['port']
        ))

        # Setup locale
        locale.setlocale(locale.LC_ALL, config['general']['locale'])

        app = rod.create_app(config)

        app.run(  # Kick off the app
            host=config['network']['host'],
            port=config['network']['port'],
            debug=config['general']['debug']
        )

    except KeyError, e:
        log.error('Requested configuration key does not exist: {}'.format(e))


if __name__ == '__main__':
    main()
