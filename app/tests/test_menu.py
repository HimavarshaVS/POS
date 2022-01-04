import unittest
from .prepare_test import SetUpTest
from .logger import Logger
from app import create_app
app = create_app()


def setUpModule():
    _log = Logger(name='test_api.log')
    _test = SetUpTest(_log)


class TestAPI(unittest.TestCase):
    log = Logger(name='test_items_api.log')
    test = SetUpTest(log)
    item_id = ''

    @classmethod
    def setUpClass(cls) -> None:
        cls.log = cls.test.log
        cls.app = cls.test.app

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_01_add_items(self):
        data = {
            "item_name": "plant based burger small",
            "description": "bun",
            "price": 6.99,
            "quantity": 500,
            "modifiers": {
                "toppings": ["Lettuce", "Tomato", "Pickles", "Onions"],
                "bun_choice": ["sesame", "whole wheat", "keto"]
            }
        }
        result = self.app.post("/v1/menu", json=data)
        self.log.info(result)
        res = result.get_json()
        item_id = res['result']['item_info']['id']
        self.assertEqual(result.status_code, 200)
        self.assertEqual(res['result']['msg'], "Item created successfully")
        self.delete_items(item_id)

    def test_02_get_items(self):
        result = self.app.get(f"/v1/menu")
        self.log.info(result)
        res = result.get_json()
        self.assertEqual(result.status_code, 200)

    def test_03_update_items(self):
        item_id = self.create_items()
        payload = {
            "price": 1.99
        }
        result = self.app.put(f"/v1/menu/{item_id}", json=payload)
        self.log.info(result)
        res = result.get_json()
        self.assertEqual(result.status_code, 200)
        self.delete_items(item_id)

    def test_04_delete_items(self):
        item_id = self.create_items()
        result = self.app.delete(f"/v1/menu/{item_id}")
        self.log.info(result)
        res = result.get_json()
        self.assertEqual(result.status_code, 200)

    def create_items(self):
        payload = {
            "item_name": "2 Mc chicken nuggets",
            "description": "nuggets",
            "price": 2.99,
            "quantity": 100,
            "modifiers": {
                "toppings": ["Lettuce", "Tomato", "Pickles", "Onions"],
                "bun_choice": ["sesame", "whole wheat", "keto"]
            }
        }
        result = self.app.post("/v1/menu", json=payload)
        res = result.get_json()
        item_id = res['result']['item_info']['id']
        return item_id

    def delete_items(self, item_id):
        result = self.app.delete(f"/v1/menu/{item_id}")
        res = result.get_json()