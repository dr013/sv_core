from django.test import TestCase
from sequences import get_next_value

from .models import *


class DictTestCase(TestCase):
    # def setUp(self):
    #     Dictionary.objects.create(name="lion", sound="roar")
    #     Animal.objects.create(name="cat", sound="meow")

    def test_dictionary_create(self):
        uid = get_next_value("dictionary")
        dictionary = Dictionary(id=uid, dict_code="test", code="0001", is_numeric=True,
                                is_editable=True, module_code="com")
        i18n = I18n(entity=dictionary, lang="")
        self.assertEqual(dictionary.dict_code, "test")
        self.assertEqual(dictionary.code, "0001")
        self.assertTrue(dictionary.is_editable)
        self.assertTrue(dictionary.is_numeric)
        self.assertEqual(dictionary.module_code, "com")
        self.assertEqual(dictionary.id, uid)

        # After save case changed to upper
        dictionary.save()

        self.assertEqual(dictionary.dict_code, "TEST")
        self.assertEqual(dictionary.module_code, "COM")
