from ..vaultkeeper_adaptor import VKAdaptor


class TestAdaptor(object):

    def setup(self):
        self.DATABASES = {}
        self.BROKER_URL = ''
        self.adaptor = VKAdaptor(config_path='./test/testconfig.json',
                                 DATABASES=self.DATABASES,
                                 BROKER_URL=self.BROKER_URL)

    def test_get_broker_url(self):
        broker = self.adaptor.data[2]
        self.adaptor.get_broker_url(broker)
        assert (self.adaptor.BROKER_URL ==
                'amqp://rtest:rpass@0.0.0.0:5672/myvhost')

    def test_get_database_configs(self):
        db = self.adaptor.data[0]
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
