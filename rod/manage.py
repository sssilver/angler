import os
import yaml
import locale
import logging
import flask.ext.script
import flask.ext.script.commands
import sqlalchemy.exc

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

except KeyError, e:
    raise SystemExit('Requested configuration key does not exist: {}'.format(e))


manager = flask.ext.script.Manager(app)
manager.add_command('server', flask.ext.script.Server())
manager.add_command('show-urls', flask.ext.script.commands.ShowUrls())
manager.add_command('clean', flask.ext.script.commands.Clean())


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


@manager.command
def createuser():
    import rod.model.staff

    # Create a user with only the basic credentials
    staff = rod.model.staff.Staff()

    staff.email = flask.ext.script.prompt('User email')
    staff.set_password(flask.ext.script.prompt_pass('User password'))

    try:
        rod.model.db.session.add(staff)
        rod.model.db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        log.error('User {} already exists'.format(staff.email))

    log.info('User {} successfully created.'.format(staff.email))
    log.info('Profile details can be entered using the web interface.')


if __name__ == '__main__':
    manager.run()
