from app import create_app


class SetUpTest:

    def __init__(self, log):
        self.log = log
        self.app = PrepareTest(log).app

    def create_items(self, item_name):
        payload = {
            "item_name": item_name,
            "description": "nuggets",
            "price": 2.99,
            "quantity": 100,
            "modifiers": {
                "toppings": ["Lettuce", "Tomato", "Pickles", "Onions"],
                "bun_choice": ["sesame", "whole wheat", "keto"]
            }
        }
        result = self.app.post("/v1/item", json=payload)
        res = result.get_json()
        if result.status_code == 200:
            return res
        else:
            self.log.error(f"Error while trying to create item : {res}")
            return None

    def delete_items(self, item_id):
        result = self.app.delete(f"/v1/menu/{item_id}")
        res = result.get_json()
        return res

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class PrepareTest(metaclass=Singleton):

    def __init__(self, log):
        self.app = self.create_test_client()
        self.log = log

    def create_test_client(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        test_client = app.test_client(self)
        return test_client