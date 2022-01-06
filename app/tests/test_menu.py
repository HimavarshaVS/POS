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
    item_res = None


    @classmethod
    def setUpClass(cls) -> None:
        cls.log = cls.test.log
        cls.app = cls.test.app
        try:
            pass
            # cls.item_res = cls.test.create_items()
            # if cls.item_res is not None:
            #     cls.item_id = cls.item_res['message']['item_info']['id']
        except Exception as error:
            cls.log.error(f"Error while creating items in set up class : {error}")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.log.info("\n")
        cls.log.info("START TEAR DOWN PROCESS")
        try:
            cls.log.info(f"Teardown process not needed")
            # cls.test.delete_items(item_id=cls.item_id)
        except Exception as error:
            cls.log.error(f"Failed to delete items created during set up ; {error}")

    def test_01_add_items(self):
        data = {
            "item_name": "plant based burger small create",
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
        item_info = self.test.create_items("update_items")
        if item_info is not None:
            item_id = item_info['message']['item_info']['id']
            item_price = item_info['message']['item_info']['price']
            payload = {
                "price": item_price*2
            }
            result = self.app.put(f"/v1/item/{item_id}", json=payload)
            self.log.info(result)
            res = result.get_json()
            self.assertEqual(result.status_code, 200)
            self.test.delete_items(item_id)

    def test_04_delete_items(self):
        item_info = self.test.create_items("item_deleted")
        item_id = item_info['message']['item_info']['id']
        result = self.app.delete(f"/v1/item/{item_id}")
        self.log.info(result)
        res = result.get_json()
        self.assertEqual(result.status_code, 200)

    def test_05_invalid_price(self):
        data = {
            "item_name": "plant based burger small",
            "description": "bun",
            "price": 0,
            "quantity": 500
        }
        result = self.app.post("/v1/item", json=data)
        self.log.info(result)
        res = result.get_json()
        errro_msg = res['validation_error']['body_params'][0]['msg']
        self.assertEqual(result.status_code, 400)
        self.assertEqual(errro_msg, "ensure this value is greater than 1")

    def test_06_invalid_item_name(self):
        data = {
            "item_name": 1,
            "description": "bun",
            "price": 0,
            "quantity": 500
        }
        result = self.app.post("/v1/item", json=data)
        self.log.info(result)
        res = result.get_json()
        errro_msg = res['message']
        self.assertEqual(result.status_code, 400)
        self.assertEqual(errro_msg, "Input payload validation failed")

    def test_07_invalid_desc(self):
        data = {
            "item_name": "ikfc chicken",
            "description": "spicy fried chicken dfsgffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffgggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg",
            "price": 1,
            "quantity": 500
        }
        result = self.app.post("/v1/item", json=data)
        self.log.info(result)
        res = result.get_json()
        errro_msg = res['validation_error']['body_params'][0]['msg']
        self.assertEqual(result.status_code, 400)
        self.assertEqual(errro_msg, "ensure this value has at most 150 characters")





