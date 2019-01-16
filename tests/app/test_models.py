from datetime import datetime

from flask_philo_core.test import FlaskPhiloTestCase, BaseTestFactory

from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UnicodeSetAttribute,
    UTCDateTimeAttribute
)

from flask_philo_pynamodb.attributes import UUIDAttribute
from flask_philo_pynamodb.models import FlaskPynamoDBModel

import random


class Thread(FlaskPynamoDBModel):
    class Meta:
        table_name = 'Thread'
    forum_name = UnicodeAttribute(hash_key=True)
    subject = UnicodeAttribute(range_key=True)
    views = NumberAttribute(default=0)
    replies = NumberAttribute(default=0)
    tags = UnicodeSetAttribute()
    last_post_datetime = UTCDateTimeAttribute()


class ModelTest(FlaskPynamoDBModel):
    class Meta:
        table_name = 'ModelTest'
    key = UUIDAttribute(hash_key=True)


class Factory(BaseTestFactory):
    @classmethod
    def create_thread(cls, **kwargs):
        params = {
            'forum_name': cls.create_unique_string(),
            'subject': cls.create_unique_string(),
            'views': random.randrange(999),
            'replies': random.randrange(999),
            'tags': [cls.create_unique_string(), cls.create_unique_string()],
            'last_post_datetime': datetime.utcnow()
        }

        for k, v in kwargs.items():
            params[k] = v

        forum_name = params.pop('forum_name')
        obj = Thread(forum_name, **params)
        obj.save()
        return obj


class TestPynamoDBModels(FlaskPhiloTestCase):
    config = {
        'AWS': {
            'AWS_REGION': 'us-west-2',
            'AWS_ACCESS_KEY_ID': BaseTestFactory.create_unique_string(),
            'AWS_SECRET_ACCESS_KEY': BaseTestFactory.create_unique_string(),
        },
        'PYNAMODB': {
            'host': 'http://db:8000'
        }

    }

    def teardown(self):
        with self.app.app_context():
            if Thread.exists():
                Thread.delete_table()

    def test_create_table(self):
        with self.app.app_context():
            assert (Thread.exists() is False)
            Thread.create_table(
                read_capacity_units=1, write_capacity_units=1, wait=True)
            assert Thread.exists()
            Thread.delete_table()
            assert (Thread.exists() is False)

    def test_create(self):
        with self.app.app_context():
            Thread.create_table(
                read_capacity_units=1, write_capacity_units=1, wait=True)
            assert 0 == Thread.count()
            Factory.create_thread()
            assert 1 == Thread.count()

    def test_get(self):
        with self.app.app_context():
            Thread.create_table(
                read_capacity_units=1, write_capacity_units=1, wait=True)
            params = {
                'forum_name': Factory.create_unique_string(),
                'subject': Factory.create_unique_string()
            }
            Factory.create_thread(**params)
            assert 1 == Thread.count()
            obj = Thread.get(params['forum_name'], params['subject'])
            assert obj.forum_name == params['forum_name']
            assert obj.subject == params['subject']

    def test_update(self):
        with self.app.app_context():
            Thread.create_table(
                read_capacity_units=1, write_capacity_units=1, wait=True)
            params = {
                'forum_name': Factory.create_unique_string(),
                'subject': Factory.create_unique_string(),
                'views': 1
            }
            Factory.create_thread(**params)
            assert 1 == Thread.count()
            obj = Thread.get(params['forum_name'], params['subject'])
            obj.views = 2
            obj.save()
            assert 1 == Thread.count()
            obj2 = Thread.get(params['forum_name'], params['subject'])
            assert obj2.views != 1
            assert obj2.views == 2

    def test_delete(self):
        with self.app.app_context():
            Thread.create_table(
                read_capacity_units=1, write_capacity_units=1, wait=True)
            params = {
                'forum_name': Factory.create_unique_string(),
                'subject': Factory.create_unique_string()
            }
            Factory.create_thread(**params)
            assert 1 == Thread.count()
            obj = Thread.get(params['forum_name'], params['subject'])
            obj.delete()
            assert 0 == Thread.count()


class TestAttributes(FlaskPhiloTestCase):
    config = {
        'AWS': {
            'AWS_REGION': 'us-west-2',
            'AWS_ACCESS_KEY_ID': BaseTestFactory.create_unique_string(),
            'AWS_SECRET_ACCESS_KEY': BaseTestFactory.create_unique_string(),
        },
        'PYNAMODB': {
            'host': 'http://db:8000'
        }

    }

    def teardown(self):
        with self.app.app_context():
            if ModelTest.exists():
                ModelTest.delete_table()

    def test_uuid(self):
        with self.app.app_context():
            assert (ModelTest.exists() is False)
            ModelTest.create_table(
                read_capacity_units=1, write_capacity_units=1, wait=True)
            assert 0 == ModelTest.count()
            key = Factory.create_uuid()
            obj = ModelTest(key)
            obj.save()
            assert 1 == ModelTest.count()
            obj2 = ModelTest.get(key)
            assert obj.key == obj2.key
