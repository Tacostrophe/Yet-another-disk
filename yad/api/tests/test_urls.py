import json
import os
from http import HTTPStatus

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from rest_framework.test import APIClient

from api.models import Item

User = get_user_model()


def setUpModule():
    global URL_NODES, URL_DELETE, URL_IMPORTS, URL_UPDATES
    URL_NODES = '/nodes/'
    URL_DELETE = '/delete/'
    URL_IMPORTS = '/imports'
    URL_UPDATES = '/updates'


class APIURLTests(TestCase):
    # @ClassMethod
    # def setUpClass(cls):
    #     super().setUpClass()

        # Создание папки и файла для теста nodes
        # Item.objects.create(
        #     id="069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
        #     type=Item.Types.FOLDER,
        #     url=None,
        #     date='2022-02-03T12:00:00Z',
        #     parent=None,
        #     size=None
        # )

    def setUp(self):
        self.guest_client = APIClient()

    def test_urls_exists_at_desired_location(self):
        '''Smoke test. Страницы возвращают ожидаемый HTTPStatus'''
        # test /imports
        test_data_dir = os.path.join(settings.BASE_DIR, 'api',
                                     'tests', 'test_data')
        test_data_json = 't_data_1.json'
        with open(os.path.join(test_data_dir, test_data_json)) as file:
            data = json.load(file)
        response = self.guest_client.post(URL_IMPORTS, data,
                                          format='json')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        print('url check /imports passed')
        # test /nodes/<id>
        for item in data.get('items'):
            url_nodes_id = URL_NODES + str(item.get('id'))
            response = self.guest_client.get(url_nodes_id, format='json')
            self.assertEqual(response.status_code, HTTPStatus.OK)
        print('url check /nodes passed')
        # test /update?<date>
        response = self.guest_client.get(URL_UPDATES, {'date': '2023-02-03T15:00:00Z'}, format='json')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.guest_client.get(URL_UPDATES, format='json')
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        print('url check /update passed')
        # test /delete/<id>?<date>
        for item in data.get('items'):
            url_delete_id = URL_DELETE + str(item.get('id'))
            print(url_delete_id)
            date = data.get('updateDate')
            print(date)
            response = self.guest_client.delete(url_delete_id, format='json')
            self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
            url_delete_id += '?date=' + str(date)
            print(url_delete_id)
            item_to_delete = Item.objects.get(id=str(item.get('id')))
            print(f'{item_to_delete.date=}')
            response = self.guest_client.delete(url_delete_id, format='json')
            print(response.content)
            self.assertEqual(response.status_code, HTTPStatus.OK,
                             '/delete doesn\'t response with expected status code')
        print('url check /delete passed')
