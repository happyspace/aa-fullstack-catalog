import sqlalchemy
from sqlalchemy import create_engine


def create_table():
    """
    >>> import sqlalchemy
    >>> from sqlalchemy import create_engine
    >>> from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
    >>> sqlalchemy.__version__
    '1.0.8'
    >>> engine = create_engine('sqlite:///tutorial.db', echo=True)
    >>> metadata = MetaData()

    >>> users = Table('users', metadata,
    ...     Column('id', Integer, primary_key=True),
    ...     Column('name', String),
    ...     Column('fullname', String),
    ... )
    >>> users.name
    'users'

    >>> addresses = Table('addresses', metadata,
    ...   Column('id', Integer, primary_key=True),
    ...   Column('user_id', None, ForeignKey('users.id')),
    ...   Column('email_address', String, nullable=False)
    ...  )
    >>> addresses.name
    'addresses'

    >>> def create_all():
    ...  metadata.create_all(engine)
    ...  return True
    >>> create_all() # doctest +IGNORE_RESULT
    True

    >>> ins = users.insert()
    >>> str(ins)
    'INSERT INTO users (id, name, fullname) VALUES (:id, :name, :fullname)'
    >>> ins = users.insert().values(name='jack', fullname='Jack Jones')
    >>> str(ins)
    'INSERT INTO users (name, fullname) VALUES (:name, :fullname)'
    >>> ins.compile().params
    {'fullname': 'Jack Jones', 'name': 'jack'}
    """
    print "tests"


def cube(x):
    """
    >>> cube(10)
    100

    >>> print range(20) # doctest: +ELLIPSIS
    [0, 1, ..., 18, 19]
    """
    return x * x


if __name__ == "__main__":
    import doctest
    import outputcheckerig

    doctest.register_optionflag(outputcheckerig.FLAG)
    doctest.OutputChecker = outputcheckerig.OutPutCheckerIR

    doctest.testmod(verbose=True)
