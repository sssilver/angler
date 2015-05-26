import distutils.core
import setuptools


distutils.core.setup(
    name='Angler Rod',
    version='2.0',
    packages=setuptools.find_packages(),

    long_description=open('README.txt').read(),
    author='Silver',
    author_email='sssilver@gmail.com',

    install_requires=[
        'tornado',
        'tornado_cors',
        'psycopg2',
        'pyyaml',
        'simplejson',
        'sqlalchemy'
    ]
)