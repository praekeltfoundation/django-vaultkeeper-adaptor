import dj_database_url
import json


def build_ids_url(backend, endpoint, identifier, secret):
    return '{0}{1}:{2}@{3}'.format(
        prefixes[backend.lower()],
        identifier,
        secret,
        endpoint
    )


class VKAdaptor(object):

    def __init__(self,
                 config_path=None,
                 DATABASES=None,
                 BROKER_URL=None,
                 ):
        self.config_path = config_path
        self.DATABASES = DATABASES
        self.BROKER_URL = BROKER_URL
        self.secrets = {}

        self.functionmap = {
            'postgresql': self.get_database_configs,
            'rabbitmq': self.get_broker_url,
        }

        try:
            with open(self.config_path) as f:
                data = json.load(f)
                self.data = data
        except IOError:
            raise IOError("Error: File {} not found.".format(
                          self.config_path))

    def process_all(self):
        for entry in self.data:
            name = entry['id']
            backend = entry['backend']
            self.secrets[name] = self.functionmap[backend](entry)

    def get_database_configs(self, secret):
        url = build_ids_url(secret['backend'],
                            secret['endpoint'],
                            secret['username'],
                            secret['password'])
        d = dj_database_url.parse(url)
        if 'set_role' in secret.keys():
            d['SET_ROLE'] = secret['set_role']
        db = {secret['id']: d}
        self.DATABASES.update(db)
        return d

    def get_broker_url(self, secret):
        url = build_ids_url(secret['backend'],
                            secret['endpoint'],
                            secret['username'],
                            secret['password'])
        self.BROKER_URL = url
        return self.BROKER_URL


prefixes = {
    'postgresql': 'postgres://',
    'rabbitmq': 'amqp://'
}

db_backends = [
    'postgresql',
]
