import json
import os

import shelve
from typing import Any

class DataRegister:
    def __init__(self) -> None:
        self._data_dictonary = {}
        self._data_shelf = shelve.open('data/data.db')

    def register_data(self, user_id, data, data_type):
        if user_id not in self._data_dictonary:
            self._data_dictonary[user_id] = {}

        self._data_dictonary[user_id][data_type] = data
        print(self._data_dictonary)

    def get_data(self, user_id):
        if user_id not in self._data_dictonary:
            return None

        return self._data_dictonary[user_id]
    
    def get_all_data(self):
        return self._data_dictonary

    def merge_data(self, user_id, data, data_type):
        if user_id not in self._data_dictonary:
            self._data_dictonary[user_id] = {}

        if data_type not in self._data_dictonary[user_id]:
            self._data_dictonary[user_id][data_type] = []

        self._data_dictonary[user_id][data_type].append(data)

    def save_dictionary(self):
        self._data_shelf['user_data'] = self._data_dictonary
        with open('data/data.txt', 'w') as file:
            json.dump(self._data_dictonary, file, indent=2)

    def load_dictionary(self):
        if os.path.exists('data.txt'):
            with open('data.txt', 'r') as file:
                tmp_dictonary = json.load(file)
                self._data_dictonary = {int(key): value for key, value in tmp_dictonary.items()}
                os.remove('data.txt')

        if not os.path.exists('data/data.txt'):
            if 'user_data' not in self._data_shelf:
                self._data_dictonary = {}
            else:
                self._data_dictonary = dict(self._data_shelf['user_data'])
            return
        with open('data/data.txt', 'r') as file:
            tmp_dictonary = json.load(file)
            self._data_dictonary = {int(key): value for key, value in tmp_dictonary.items()}

    def get_all_users(self):
        return self._data_dictonary.keys()

data_register = DataRegister()
