import distutils.core
import setuptools


distutils.core.setup(
    name='Angler Rod',
    version='2.0',
    packages=setuptools.find_packages(),

    long_description=open('README.txt').read(),
    author='Silver',
    author_email='sssilver@gmail.com',

    install_requires={
        'flask'
        'flask-login',
        'flask-script',
        'flask-cors',
        'flask-sqlalchemy',
        'flask-bcrypt',
        'pyyaml',
        'psycopg2',
        'sqlalchemy',
        'marshmallow-sqlalchemy',
        'python-dateutil'
    }
)
