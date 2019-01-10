from flask_philo_core.test import FlaskPhiloTestCase, BaseTestFactory

from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UnicodeSetAttribute, UTCDateTimeAttribute
)

import os
from pynamodb.models import MetaModel
from flask import current_app
from flask_philo_core import ConfigurationError

from pynamodb.connection import Connection
from pynamodb.connection.table import TableConnection
from pynamodb.constants import META_CLASS_NAME


def resolv_environment():
    """
    AWS configuration parameters such as AWS credentials
    can de defined by using environ variables or
    configuration file
    """

    attrs = {}
    app = current_app._get_current_object()
    aws_config = app.config.get('AWS', {})

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


    return attrs

class CustomMeta(MetaModel):
    def __init__(cls, name, bases, attrs):

        #env = resolv_environment()
        #region = env['AWS_REGION']
        #host = "http://db:8001"
        #aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
        #aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
        cls.Meta.table_name = cls.__tablename__
        app = current_app._get_current_object()
        super(CustomMeta, cls).__init__(name, bases, attrs)




class BaseModel(Model):

    @classmethod
    def _get_connection(cls):
        """
        Returns a (cached) connection
        """
        env = resolv_environment()
        #import ipdb; ipdb.set_trace()

        return  TableConnection('hola')


class Thread(Model):
    __tablename__ = 'Thread1'
    class Meta:
        table_name = 'Thread1'
        write_capacity_units = 10
        read_capacity_units = 10
        host = "http://db:8001"
    forum_name = UnicodeAttribute(hash_key=True)
    subject = UnicodeAttribute(range_key=True)
    views = NumberAttribute(default=0)
    replies = NumberAttribute(default=0)
    answered = NumberAttribute(default=0)
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
