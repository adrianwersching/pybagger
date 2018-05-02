import json

import requests

from bag_status import BagStatus
from fruit import Fruit


class Fruitbagger:

    def __init__(self, auth_key):
        self._url = "https://fruitbagger.herokuapp.com"
        self._header = {"auth": auth_key}

        self._session_url = "/api/session"
        self._fruits_url = "/api/fruits"
        self._bag_url = "/api/bag"
        self._bagging_url = "/api/bagging"

        self._session = None
        self._bag = None

    def open_session(self):
        url = self._url + self._session_url
        self._session = requests.post(url=url, headers=self._header).content.decode("utf-8")
        print("Opened session " + self._session)

    def close_session(self):
        url = self._url + self._session_url + "/" + self._session
        requests.put(url=url, headers=self._header)
        print("Closed session " + self._session)

    def open_bag(self):
        url = self._url + self._bag_url + "/" + self._session
        self._bag = requests.post(url=url, headers=self._header).content.decode("utf-8")
        print("Opened bag " + self._bag)

    def close_bag(self):
        url = self._url + self._bag_url + "/" + self._session + "/" + self._bag
        requests.put(url=url, headers=self._header)
        print("Closed bag " + self._bag)

    def get_fruit(self):
        url = self._url + self._fruits_url + "/" + self._session
        response = requests.get(url=url, headers=self._header)
        if response.status_code == 400:
            return None, BagStatus.LOOKAHEAD_EXCEEDED
        elif response.status_code == 204:
            return None, BagStatus.NO_MORE_FRUITS

        fruit = json.loads(response.content.decode("utf-8"))
        key = "".join(fruit.keys())
        value = fruit[key]
        fruit = Fruit(key, value)
        print("Retrieved fruit " + fruit.key)
        return fruit, BagStatus.OK

    def bag_fruit(self, fruit):
        url = self._url + self._bagging_url + "/" + self._session + "/" + self._bag + "/" + fruit.key
        requests.post(url=url, headers=self._header)
        print("Bagged fruit " + fruit.key)
