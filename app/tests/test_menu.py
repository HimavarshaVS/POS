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
        try:
            cls.log.info(f"No deletion required")
        except Exception as error:
            cls.log.error(f"Error while creating items in set up class : {error}")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.log.info("\n")
        cls.log.info("START TEAR DOWN PROCESS")
        try:
            cls.test.delete_items(item_id=cls.item_id)
        except Exception as error:
            cls.log.error(f"Failed to delete items created during set up ; {error}")

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
        result = self.app.post("/v1/item", json=data)
        self.log.info(result)
        res = result.get_json()
        item_id = res['message']['item_info']['id']
        self.assertEqual(result.status_code, 200)
        self.assertEqual(res['message']['msg'], "Item created successfully")
        self.test.delete_items(item_id)

    def test_02_get_items(self):
        result = self.app.get(f"/v1/items")
        self.log.info(result)
        res = result.get_json()
        self.assertEqual(result.status_code, 200)

    def test_03_update_items(self):
        # item_id = self.create_items()
        payload = {
            "price": 1.99
        }
        result = self.app.put(f"/v1/item/{self.item_id}", json=payload)
        self.log.info(result)
        res = result.get_json()
        self.assertEqual(result.status_code, 200)

    def test_04_delete_items(self):
        result = self.app.delete(f"/v1/item/{self.item_id}")
        self.log.info(result)
        res = result.get_json()
        self.assertEqual(result.status_code, 200)



