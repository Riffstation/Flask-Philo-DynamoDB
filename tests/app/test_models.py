from flask_philo_core.test import FlaskPhiloTestCase, BaseTestFactory

from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UnicodeSetAttribute, UTCDateTimeAttribute
)

import os
from pynamodb.models import MetaModel

class CustomMeta(MetaModel):
    def __init__(cls, name, bases, attrs):
        import ipdb; ipdb.set_trace()
        super(CustomMeta, cls).__init__(name, bases, attrs)

    region = os.environ['AWS_REGION']
    host = "http://db:8001"
    aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
    aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']


class BaseModel(Model, metaclass=CustomMeta):
    class Meta:
        region = os.environ['AWS_REGION']
        host = "http://db:8001"
        aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
        aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']

    @classmethod
    def _get_connection(cls):
        """
        Returns a (cached) connection
        """
        cls.Meta.table_name = cls.__tablename__
        import ipdb; ipdb.set_trace()
        super(BaseModel, cls)._get_connection()


class Thread(BaseModel):
    __tablename__ = 'Thread1'
    class Meta1:
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
        Thread.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
        Thread.delete_table()
        print('aaaaaaaaaaaaaaaaaaaaaa')
