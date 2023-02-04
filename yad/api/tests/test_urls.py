import json
import os
from http import HTTPStatus

from django.conf import settings
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from api.models import Item


def setUpModule():
    global URL_NODES, URL_DELETE, URL_IMPORTS, URL_UPDATES
    global TEST_DATA_DIR, TEST_FOLDER_ID, DATETIME_FORMAT
    URL_NODES = "/nodes"
    URL_DELETE = "/delete"
    URL_IMPORTS = "/imports"
    URL_UPDATES = "/updates"
    TEST_DATA_DIR = os.path.join(
        settings.BASE_DIR, "api", "tests", "test_data"
    )
    TEST_FOLDER_ID = "069cb8d7-bbdd-47d3-ad8f-82ef4c269df2"
    DATETIME_FORMAT = settings.REST_FRAMEWORK.get("DATETIME_FORMAT")


class APIURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Создание item для тестов nodes и delete
        Item.objects.create(
            id=TEST_FOLDER_ID,
            type=Item.Types.FOLDER,
            url=None,
            date=timezone.now().strftime(DATETIME_FORMAT),
            parent=None,
            size=None,
        )

    def setUp(self):
        self.guest_client = APIClient()

    def test_url_imports_exists_at_desired_location(self):
        """Smoke test. /imports возвращает ожидаемый HTTPStatus"""
        test_data_json = "t_data_1.json"
        with open(os.path.join(TEST_DATA_DIR, test_data_json)) as file:
            data = json.load(file)
        response = self.guest_client.post(URL_IMPORTS, data, format="json")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        print("url check /imports passed")

    def test_url_nodes_exists_at_desired_location(self):
        """Smoke test. /nodes возвращает ожидаемый HTTPStatus"""
        item = Item.objects.get(id=TEST_FOLDER_ID)
        url_nodes_id = URL_NODES + "/" + str(item.id)
        response = self.guest_client.get(url_nodes_id, format="json")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        print("url check /nodes passed")

    def test_url_update_exists_at_desired_location(self):
        """Smoke test. /update возвращает ожидаемый HTTPStatus"""
        response = self.guest_client.get(
            URL_UPDATES,
            {"date": timezone.now().strftime(DATETIME_FORMAT)},
            format="json",
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.guest_client.get(URL_UPDATES, format="json")
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        print("url check /update passed")

    def test_url_delete_exists_at_desired_location(self):
        """Smoke test. /delete возвращает ожидаемый HTTPStatus"""
        item = Item.objects.get(id=TEST_FOLDER_ID)
        url_delete_id = URL_DELETE + "/" + str(item.id)
        response = self.guest_client.delete(url_delete_id, format="json")
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        url_delete_id += "?date=" + str(item.date)
        response = self.guest_client.delete(url_delete_id, format="json")
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK,
            "/delete doesn't response with expected status code",
        )
        print("url check /delete passed")
