import os
import json

from django.conf import settings
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from api import views


def setUpModule():
    global TEST_DATA_DIR
    TEST_DATA_DIR = os.path.join(
        settings.BASE_DIR, "api", "tests", "test_data"
    )


class APISerializerTest(TestCase):
    def test_imports_validate(self):
        """Проверка валидации /imports"""
        factory = APIRequestFactory()
        test_data_json = "t_data_2.json"
        with open(os.path.join(TEST_DATA_DIR, test_data_json)) as file:
            data = json.load(file)
        request = factory.post("/imports", data, format="json")
        imports_view = views.ImportsView.as_view()
        response = imports_view(request)
        request_date = data.get("updateDate")
        response_date = response.data.get("updateDate")
        self.assertEqual(request_date, response_date)
        request_items = data.get("items")
        response_items = response.data.get("items")
        self.assertEqual(len(request_items), len(response_items))
        for response_item in response_items:
            request_item = None
            for key, response_value in response_item.items():
                if not request_item:
                    for i in range(len(request_items)):
                        item = request_items[i]
                        item_id = item.get("id")
                        response_item_id = response_item.get("id")
                        if item_id == response_item_id:
                            request_item = request_items.pop(i)
                            break
                    else:
                        raise AssertionError("no response with requested file")
                if key == "date":
                    request_value = request_date
                elif key == "size":
                    # checked in test_models
                    continue
                else:
                    request_value = request_item.get(key)
                self.assertEqual(
                    request_value,
                    response_value,
                    f"{key} doesn't create properly",
                )
