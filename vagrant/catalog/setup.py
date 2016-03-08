from setuptools import setup

install_requires = [
    'alembic==0.8.4',
    'bleach==1.4.2',
    'colorama==0.3.6',
    'Flask==0.10.1',
    'html5lib==0.9999999',
    'httplib2==0.9.2',
    'itsdangerous==0.24',
    'Jinja2==2.8',
    'Mako==1.0.3',
    'MarkupSafe==0.23',
    'oauth2client==2.0.0.post1',
    'Pillow==3.1.1',
    'pluggy==0.3.1',
    'psycopg2==2.6.1',
    'py==1.4.31'
    'pyasn1==0.1.9',
    'pyasn1-modules==0.0.8',
    'python-dateutil==2.4.2',
    'python-editor==0.5',
    'requests==2.9.1',
    'rsa==3.3',
    'six==1.10.0',
    'SQLAlchemy==1.0.12',
    'SQLAlchemy-Utils==0.31.6',
    'tox==2.3.1',
    'typing==3.5.0.1',
    'virtualenv==14.0.6',
    'Werkzeug==0.11.4',
    'wheel==0.29.0',
]

setup(
    name='catalog',
    version='1.0.0',
    packages=[''],
    py_modules={'catalog': './project',
                'play': './sample'},
    package_dir={'catalog': './project'},
    url='',
    license='',
    author='Eddie Warner',
    author_email='happyspace@gmail.com',
    description='Catalog project for Udacity Fullstack nano degree. '
)
