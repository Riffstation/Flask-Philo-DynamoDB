from flask_philo_core.test import FlaskPhiloTestCase, BaseTestFactory

from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UnicodeSetAttribute, UTCDateTimeAttribute
)

import os
from pynamodb.models import MetaModel
from flask import current_app
from flask_philo_core import ConfigurationError
from pynamodb.settings import get_settings_value
from pynamodb.connection import Connection
from pynamodb.connection.table import TableConnection
from pynamodb.constants import META_CLASS_NAME, REGION, HOST


from types import *

def resolv_environment():
    """
    AWS configuration parameters such as AWS credentials
    can de defined by using environ variables or
    configuration file. PyNAMoDb settings should be
    defined in the configuration file
    """

    attrs = {}
    app = current_app._get_current_object()
    aws_config = app.config.get('AWS', {})
    pynamo_config = app.config.get('PYNAMODB', {})

    if 'AWS_REGION' in aws_config:
        attrs['AWS_REGION'] = aws_config['AWS_REGION']

    elif 'AWS_REGION' in os.environ:
        attrs['AWS_REGION'] = os.environ['AWS_REGION']

    else:
        raise ConfigurationError('AWS_REGION undefined')

    if 'AWS_ACCESS_KEY_ID' in aws_config:
        attrs['AWS_ACCESS_KEY_ID'] = aws_config['AWS_ACCESS_KEY_ID']

    elif 'AWS_ACCESS_KEY_ID' in os.environ:
        attrs['AWS_ACCESS_KEY_ID'] = os.environ['AWS_ACCESS_KEY_ID']

    else:
        raise ConfigurationError('AWS_ACCESS_KEY_ID undefined')

    if 'AWS_SECRET_ACCESS_KEY' in aws_config:
        attrs['AWS_SECRET_ACCESS_KEY'] = aws_config['AWS_SECRET_ACCESS_KEY']

    elif 'AWS_ACCESS_KEY_ID' in os.environ:
        attrs['AWS_SECRET_ACCESS_KEY'] = os.environ['AWS_SECRET_ACCESS_KEY']

    else:
        raise ConfigurationError('AWS_SECRET_ACCESS_KEY undefined')

    if HOST in pynamo_config:
        attrs['HOST'] = pynamo_config[HOST]
    else:
        attrs['HOST'] = get_settings_value('host')


    return attrs


def _get_connection(cls):
    env = resolv_environment()
    import ipdb; ipdb.set_trace()
    if not hasattr(cls.Meta, REGION):
        setattr(cls.Meta, REGION, env.get('AWS_REGION'))

    if not hasattr(cls.Meta, HOST):
        setattr(attr_obj, HOST, get_settings_value('host'))

    if not hasattr(attr_obj, 'session_cls'):
        setattr(attr_obj, 'session_cls', get_settings_value('session_cls'))
    if not hasattr(attr_obj, 'request_timeout_seconds'):
        setattr(attr_obj, 'request_timeout_seconds', get_settings_value('request_timeout_seconds'))
    if not hasattr(attr_obj, 'base_backoff_ms'):
        setattr(attr_obj, 'base_backoff_ms', get_settings_value('base_backoff_ms'))
    if not hasattr(attr_obj, 'max_retry_attempts'):
        setattr(attr_obj, 'max_retry_attempts', get_settings_value('max_retry_attempts'))
    if not hasattr(attr_obj, 'aws_access_key_id'):
        setattr(attr_obj, 'aws_access_key_id', None)
    if not hasattr(attr_obj, 'aws_secret_access_key'):
        setattr(attr_obj, 'aws_secret_access_key', None)



class CustomMeta(MetaModel):
    _connection = None
    def __init__(cls, name, bases, attrs):

        #patch(cls, _get_connection)
        cls._get_connection = MethodType(_get_connection, cls)

        #env = resolv_environment()
        #region = env['AWS_REGION']
        #host = "http://db:8001"
        #aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
        #aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
        #cls.Meta.table_name = cls.__tablename__
        attrs[META_CLASS_NAME] = CustomMeta
        #setattr(cls, '_connection', False)
        #setattr(cls, '_get_connection', CustomMeta._get_connection)
        #setattr(cls, '_get_connection', _get_connection)

        app = current_app._get_current_object()
        #import ipdb; ipdb.set_trace()
        super(CustomMeta, cls).__init__(name, bases, attrs)




    @classmethod
    def _get_connection1(cls):
        cls._connection = TableConnection(cls.Meta.table_name,
                                          region=cls.Meta.region,
                                          host=cls.Meta.host,
                                          session_cls=cls.Meta.session_cls,
                                          request_timeout_seconds=cls.Meta.request_timeout_seconds,
                                          max_retry_attempts=cls.Meta.max_retry_attempts,
                                          base_backoff_ms=cls.Meta.base_backoff_ms,
                                          aws_access_key_id=cls.Meta.aws_access_key_id,
                                          aws_secret_access_key=cls.Meta.aws_secret_access_key)
    @classmethod
    def _get_connection3(cls):
        """
        Returns a (cached) connection
        """
        env = resolv_environment()
        import ipdb; ipdb.set_trace()
        return  TableConnection('hola')



class BaseModel(Model):

    @classmethod
    def _get_connection(cls):
        """
        Returns a (cached) connection
        """
        env = resolv_environment()
        #import ipdb; ipdb.set_trace()
        return  TableConnection('hola')


class Thread(Model, metaclass=CustomMeta):
    __tablename__ = 'Thread1'
    class Meta1:
        write_capacity_units = 10
        read_capacity_units = 10
        host = "http://db:8001"
    forum_name = UnicodeAttribute(hash_key=True)
    subject = UnicodeAttribute(range_key=True)
    views = NumberAttribute(default=0)
    replies = NumberAttribute(default=0)
    tags = UnicodeSetAttribute()
    last_post_datetime = UTCDateTimeAttribute()


class TestModels(FlaskPhiloTestCase):


    def test_get_example(self):
        config =  {
            'AWS': {
                'AWS_REGION': 'us-west-2',
                'AWS_ACCESS_KEY_ID': BaseTestFactory.create_unique_string(),
                'AWS_SECRET_ACCESS_KEY': BaseTestFactory.create_unique_string(),
            }

        }

        app = BaseTestFactory.create_test_app(config=config)
        with app.app_context():
            Thread.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
        #    Thread.delete_table()
        #    print('aaaaaaaaaaaaaaaaaaaaaa')
