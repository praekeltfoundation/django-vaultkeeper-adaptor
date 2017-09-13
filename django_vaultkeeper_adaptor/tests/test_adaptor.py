import pytest
from ..vaultkeeper_adaptor import VKAdaptor

class TestAdaptor(object):

    def setup(self):
        self.data = [
            {
                'id': 'default',
                'backend': 'postgresql',
                'endpoint': '0.0.0.0:5432/mydb',
                'vault_path': 'database/creds/psql-rw',
                'schema': 'public',
                'policy': 'psql-rw',
                'set_role': 'app_owner',
                'username': 'ptest',
                'password': 'ppass',
                'lease_duration': 100,
                'renewable': True,
            },
            {
                'id': 'auxiliary',
                'backend': 'postgresql',
                'endpoint': '1.1.1.1:5432/mydb1',
                'vault_path': 'database/creds/psql-rw-ax',
                'schema': 'public',
                'policy': 'psql-rw-ax',
                'set_role': 'app_owner1',
                'username': 'ptest1',
                'password': 'ppass1',
                'lease_duration': 100,
                'renewable': True,
            },
            {
                'id': 'broker1',
                'backend': 'rabbitmq',
                'endpoint': '0.0.0.0:5672/myvhost',
                'vault_path': '/rabbitmq/creds/ampq-worker',
                'username': 'rtest',
                'password': 'rpass',
                'vhost': 'myvhost',
                'policy': 'ampq-worker',
            }
        ]
        self.DATABASES = {}
        self.BROKER_URL = ''
        self.adaptor = VKAdaptor(data=self.data,
                                     DATABASES=self.DATABASES,
                                     BROKER_URL=self.BROKER_URL)

    def test_get_broker_url(self):
        broker = self.data[2]
        self.adaptor.get_broker_url(broker)
        assert (self.adaptor.BROKER_URL ==
                'amqp://rtest:rpass@0.0.0.0:5672/myvhost')

    def test_get_database_configs(self):
        db = self.data[0]
        self.adaptor.get_database_configs(db)
        assert self.adaptor.DATABASES == {
             'default': {
                 'ENGINE': 'django.db.backends.postgresql_psycopg2',
                 'NAME': 'mydb',
                 'USER': 'ptest',
                 'PASSWORD': 'ppass',
                 'HOST': '0.0.0.0',
                 'PORT': 5432,
                 'SET_ROLE': 'app_owner',
                 'CONN_MAX_AGE': 0,
             }
        }

    def test_process_all(self):
        self.adaptor.process_all()
        assert self.adaptor.secrets == {
            'broker1': 'amqp://rtest:rpass@0.0.0.0:5672/myvhost',
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'mydb',
                'USER': 'ptest',
                'PASSWORD': 'ppass',
                'HOST': '0.0.0.0',
                'PORT': 5432,
                'SET_ROLE': 'app_owner',
                'CONN_MAX_AGE': 0,
            },
            'auxiliary': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'mydb1',
                'USER': 'ptest1',
                'PASSWORD': 'ppass1',
                'HOST': '1.1.1.1',
                'PORT': 5432,
                'SET_ROLE': 'app_owner1',
                'CONN_MAX_AGE': 0,
            }
        }
