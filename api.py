import os

import requests
from key_services import get_token


def parametrized(dec):
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)

        return repl

    return layer


def token_update(func):
    def wrapper(*args, **kwargs):
        os.environ['IAM_TOKEN'] = get_token()['iamToken']
        return func(*args, **kwargs)

    return wrapper


def iam():
    return os.environ.get('IAM_TOKEN')


@token_update
def post_request(url, json=None, headers=dict()):
    headers['Authorization'] = f'Bearer {iam()}'
    response = requests.post(url, json=json, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'API ERROR: {response} {response.text}')
        return 'error'


@token_update
def get_request(url, json=None, headers=dict()):
    headers['Authorization'] = f'Bearer {iam()}'
    response = requests.get(url, json=json, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'API ERROR: {response} {response.text}')
        return 'error'


class YandexCloudApi:
    def __init__(self):
        pass

    def start_instance(self, instanceId):
        return post_request(f'https://compute.api.cloud.yandex.net/compute/v1/instances/{instanceId}:start')

    def stop_instance(self, instanceId):
        return post_request(f'https://compute.api.cloud.yandex.net/compute/v1/instances/{instanceId}:stop')

    def restart_instance(self, instanceId):
        return post_request(f'https://compute.api.cloud.yandex.net/compute/v1/instances/{instanceId}:restart')

    def get_instance(self, instanceId):
        return get_request(f'https://compute.api.cloud.yandex.net/compute/v1/instances/{instanceId}')

    def get_status(self, instanceId):
        return self.get_instance(instanceId)['status']

    def get_instances(self):
        return get_request(f'https://compute.api.cloud.yandex.net/compute/v1/instances',
                           json={'folderId': 'b1g4dkb7kl9jb5vciu0k'})

    def get_filtered_instances(self, query):
        """
        :param query: List with rules, example ["instance['status'] == 'RUNNING'"]
        :return: Filtered instances
        """

        data = self.get_instances()['instances']
        for rule in query:
            data = filter(lambda instance: eval(rule, {'instance': instance}), data)
        return tuple(data)


yc = YandexCloudApi()  # Создания экземпляра API

all_VMs = yc.get_instances()  # Получение списка всех виртуальных машин

for vm in all_VMs:
    yc.start_instance(vm['id'])  # Запуск виртуальной машины

