import os
import yaml
import locale
import logging
import flask.ext.script
import flask.ext.script.commands

import rod
import rod.model
import rod.model.staff


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('rod')


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

    manager = flask.ext.script.Manager(app)
    manager.add_command('server', flask.ext.script.Server())
    manager.add_command('show-urls', flask.ext.script.commands.ShowUrls())
    manager.add_command('clean', flask.ext.script.commands.Clean())

except KeyError, e:
    log.error('Requested configuration key does not exist: {}'.format(e))


@manager.shell
def make_shell_context():
    return dict(app=app, db=rod.model.db, User=rod.model.staff.Staff)


@manager.command
def createdb():
    # Import all models
    import rod.model.comment
    import rod.model.company
    import rod.model.course
    import rod.model.group
    import rod.model.lesson
    import rod.model.level
    import rod.model.staff
    import rod.model.student
    import rod.model.tariff
    import rod.model.transaction

    rod.model.db.init_schema()


if __name__ == '__main__':
    manager.run()
