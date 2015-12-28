import distutils.core
import setuptools


distutils.core.setup(
    name='Angler Rod',
    version='2.0',
    packages=setuptools.find_packages(),

    long_description=open('README.txt').read(),
    author='sssilver',
    author_email='sssilver@gmail.com',

    install_requires={
        'flask>=0.10',
        'flask-login',
        'flask-script',
        'flask-cors',
        'flask-sqlalchemy',
        'flask-bcrypt',
        'simplejson',
        'pyyaml',
        'psycopg2',
        'sqlalchemy',
        'marshmallow-sqlalchemy',
        'python-dateutil'
    },

    entry_points = {
        'console_scripts': [
            'angler-rod = manage:main',
        ],
    }
)
