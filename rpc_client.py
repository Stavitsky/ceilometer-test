import random
import uuid
import datetime
import string
import sys
import pprint
import oslo.messaging
from oslo.config import cfg
from ceilometer.publisher import utils


def rand_counter_name():
    counter_names = ['disk.read.requests.rate',
                     'disk.read.requests',
                     'instance',
                     'cpu',
                     'disk.write.requests',
                     'instance:m1.tiny',
                     'disk.read.bytes.rate',
                     'disk.read.bytes',
                     'cpu_util',
                     'disk.write.requests.rate',
                     'disk.write.bytes.rate',
                     'disk.write.bytes',
                     'network.services.firewall',
                     'image',
                     'image.size',
                     'network.services.firewall.policy',
                     'memory',
                     'vcpus',
                     'disk.ephemeral.size',
                     'disk.root.size',
                     'network.outgoing.packets',
                     'disk.device.read.requests',
                     'disk.device.read.bytes',
                     'network.outgoing.bytes',
                     'disk.device.write.bytes',
                     'network.incoming.bytes',
                     'disk.device.write.requests',
                     'network.incoming.packets',
                     'network.outgoing.bytes.rate',
                     'network.incoming.bytes.rate',
                     'network.incoming.packets.rate',
                     'network.outgoing.packets.rate']
    return random.choice(counter_names)


def rand_user_id():
    return str(uuid.uuid4())


def rand_string(length):
    return (''.join(random.choice(string.lowercase + string.digits)
                    for i in range(length)))


def rand_resource_id():
    return str(uuid.uuid4())


def rand_message_id():
    return str(uuid.uuid4())


def rand_source():
    # add some new if exist
    sources = ['openstack']
    return random.choice(sources)


def rand_counter_unit():
    counter_units = ['packet',
                     'policy',
                     'request/s',
                     'MB',
                     'vcpu',
                     'firewall',
                     'ns',
                     'request',
                     'B',
                     'instance',
                     'GB',
                     'B/s',
                     'image',
                     'packet/s',
                     '%']

    return random.choice(counter_units)


def rand_counter_volume():
    return random.randrange(10000000, 20000000)


def rand_project_id():
    return str(uuid.uuid4())


def random_resource_metadata():
    return {'status': '',
            'name': '',
            'deleted': random.choice([True, False]),
            'container_format': random.choice(['bare', 'another_format']),
            'created_at': datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            'disk_format': random.choice(['qcow2']),
            'update_at': datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            'properties': {},
            'protected': random.choice([True, False]),
            'checksum': '133eae9fb1c98f45894a4e60d8736619',
            'min_disk': random.randrange(0, 1024),
            'is_public': random.choice([True, False]),
            'deleted_at': random.choice([True, False]),
            'min_ram': random.randrange(0, 1024),
            'size': random.randrange(10000000, 20000000)
            }


def random_counter_type():
    counter_types = ['gauge', 'cumulative']
    return random.choice(counter_types)


def generate_random_sample():
    sample = {'source': rand_source(),
              'counter_name': rand_counter_name(),
              'counter_type': random_counter_type(),
              'counter_unit': rand_counter_unit(),
              'counter_volume': rand_counter_volume(),
              'user_id': rand_user_id(),
              'project_id': rand_project_id(),
              'resource_id': rand_resource_id(),
              'timestamp': datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
              'resource_metadata': random_resource_metadata(),
              'message_id': rand_message_id()
              }
    sample['message_signature'] = utils.compute_signature(
        sample, '0680372fc6a43c4339cd')
    return sample


def collect_generated_samples(number):
    return [generate_random_sample() for i in range(number)]

context = {
    'instance_uuid': None,
    'domain': None,
    'project_domain': None,
    'auth_token': 'admin',
    'is_admin': True,
    'user': 'admin',
    'tenant': None,
    'read_only': False,
    'show_deleted': False,
    'user_identity': 'admin----',
    'request_id': 'req-13be09ac-73aa-4f03-bf82-5290047c7cff',
    'user_domain': None
}

time_before_gen = datetime.datetime.utcnow()
meters = collect_generated_samples(int(sys.argv[1]))
notifier = oslo.messaging.Notifier(
    oslo.messaging.get_transport(cfg.CONF),
    driver='messagingv2',
    publisher_id='metering.publisher.controller1',
    topic='metering'
)
notifier.sample(context, event_type='metering', payload=meters)
time_after_gen = datetime.datetime.utcnow()
print("\n{} samples was generating for {}s".format( int(sys.argv[1]),
    time_after_gen - time_before_gen))

