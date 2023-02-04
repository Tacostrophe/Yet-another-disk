from django.conf import settings
from django.test import TestCase
from django.utils import timezone

from ..models import Item


class APIModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.item = Item.objects.create(
            id="069cb8d7-bbdd-47d3-ad8f-82ef4c269df2",
            type=Item.Types.FOLDER,
            url=None,
            date=timezone.now().strftime(
                settings.REST_FRAMEWORK.get("DATETIME_FORMAT")
            ),
            parent=None,
            size=None,
        )

    def test_model_have_correct_object_name(self):
        """Проверяем, что у модели корректно работает __str__."""
        model_str = {
            APIModelTest.item: (
                str(APIModelTest.item.type) + " - " + str(APIModelTest.item.id)
            ),
        }
        for model, expected_model_name in model_str.items():
            with self.subTest(model=model):
                self.assertEqual(expected_model_name, str(model))
