from django.conf import settings
from django.test import TestCase
from django.utils import timezone

from ..models import Item


def setUpModule():
    global DATETIME_FORMAT
    DATETIME_FORMAT = settings.REST_FRAMEWORK.get("DATETIME_FORMAT")


class APIModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.folder = Item.objects.create(
            id="069cb8d7-bbdd-47d3-ad8f-82ef4c269df2",
            type=Item.Types.FOLDER,
            url=None,
            date=timezone.now().strftime(DATETIME_FORMAT),
            parent=None,
            size=None,
        )
        cls.file_1 = Item.objects.create(
            id="069cb8d7-bbdd-47d3-ad8f-82ef4c269df3",
            type=Item.Types.FILE,
            url="/file/url1",
            date=timezone.now().strftime(DATETIME_FORMAT),
            parent=cls.folder,
            size=6,
        )

    def test_model_have_correct_object_name(self):
        """Проверяем, что у модели корректно работает __str__."""
        model_str = {
            APIModelTest.folder: (
                str(APIModelTest.folder.type)
                + " - "
                + str(APIModelTest.folder.id)
            ),
        }
        for model, expected_model_name in model_str.items():
            with self.subTest(model=model):
                self.assertEqual(expected_model_name, str(model))

    def test_folder_size_works_correctly(self):
        """Проверка, что размер папки работает корректно"""
        expected_folder_size = APIModelTest.file_1.size
        error_msg = "folder size calculator doesn't work properly"
        self.assertEqual(
            APIModelTest.folder.size, expected_folder_size, error_msg
        )
        file_2_size = 4
        file_2 = Item.objects.create(
            id="069cb8d7-bbdd-47d3-ad8f-82ef4c269df4",
            type=Item.Types.FILE,
            url="/file/url2",
            date=timezone.now().strftime(DATETIME_FORMAT),
            parent=APIModelTest.folder,
            size=file_2_size,
        )
        expected_folder_size += file_2_size
        self.assertEqual(
            APIModelTest.folder.size, expected_folder_size, error_msg
        )
        file_2.delete()
        expected_folder_size -= file_2_size
        self.assertEqual(
            APIModelTest.folder.size, expected_folder_size, error_msg
        )
