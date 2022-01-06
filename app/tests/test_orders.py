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

    @classmethod
    def tearDownClass(cls) -> None:
        cls.log.info("\n")
        cls.log.info("START TEAR DOWN PROCESS")
        try:
            cls.test.delete_items(item_id=cls.item_id)
        except Exception as error:
            cls.log.error(f"Failed to delete items created during set up ; {error}")

    def test_01_create_orders(self):
        item_info = self.test.create_items("update_items")
        if item_info is not None:
            data = {
                "items": [
                    {
                        "item_id": item_info['message']['item_info']['id'],
                        "quantity": 1
                    }
                ],
                "payment_amount": (2 * self.price),
                "order_note": "spicy"
            }
            result = self.app.post("/v1/order", json=data)
            self.log.info(result)
            res = result.get_json()
            self.assertEqual(result.status_code, 200)
            # self.test.delete_items(item_id)
