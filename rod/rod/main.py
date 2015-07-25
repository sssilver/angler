import tornado.web
import tornado.ioloop
import os
import yaml
import locale
import logging

import rod.db
import rod.handler.student
import rod.handler.course
import rod.handler.level
import rod.handler.tariff
import rod.handler.staff
import rod.handler.company
import rod.handler.comment
import rod.handler.login
import rod.handler.verify


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('rod')


class Rod(tornado.web.Application):
    def __init__(self, config):
        self.config = config
        self.db = rod.db.Database(self.config['db']['uri'])

        prefix = '/api/v2'

        handlers = [(
            r'{}/student/?(\w+)?/?(\w+)?'.format(prefix),
            rod.handler.student.StudentHandler
        ), (
            r'{}/company/?(\w+)?/?(\w+)?'.format(prefix),
            rod.handler.company.CompanyHandler
        ), (
            r'{}/course/?(\w+)?/?(\w+)?'.format(prefix),
            rod.handler.course.CourseHandler
        ), (
            r'{}/tariff/?(\w+)?/?(\w+)?'.format(prefix),
            rod.handler.tariff.TariffHandler
        ), (
            r'{}/level/?(\w+)?/?(\w+)?'.format(prefix),
            rod.handler.level.LevelHandler
        ), (
            r'{}/staff/?(\w+)?/?(\w+)?'.format(prefix),
            rod.handler.staff.StaffHandler
        ), (
            r'{}/login'.format(prefix),
            rod.handler.login.LoginHandler
        ), (
            r'{}/verify'.format(prefix),
            rod.handler.verify.VerifyHandler
        )]

        super(Rod, self).__init__(
            handlers,
            **self.config.get('tornado', {})
        )


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

        # Instantiate the app class
        Rod(config).listen(config['network']['port'])

        # Kick off Tornado
        tornado.ioloop.IOLoop.current().start()

    except KeyError, e:
        log.error('Requested configuration key does not exist: {}'.format(e))


if __name__ == '__main__':
    main()
