from atexit import register
import json
import os

import shelve
from typing import Any

class DataRegister:
    def __init__(self) -> None:
        self._data_dictonary = {}
        if not os.path.exists('data'):
            os.mkdir('data')
        self._data_shelf = shelve.open('data/data.db')

    def register_user(self, user_id: int) -> None:
        if user_id in self._data_dictonary:
            return
        
        self._data_dictonary[user_id] = {}

    def _get_user_object(self, user_id: int) -> dict:
        self.register_user(user_id)
        
        return self._data_dictonary[user_id]

    def set_user_info(self, user_id: int, info: dict) -> None:
        self._get_user_object(user_id)['info'] = info

    def add_user_servey(self, user_id: int, servey: dict) -> None:
        uo = self._get_user_object(user_id)
        
        if 'servey' not in uo:
            uo['servey'] = []
        servey_list = uo['servey']
        
        servey_list.append(servey)

    def get_user_info(self, user_id: int) -> dict:
        return self._get_user_object(user_id).get('info', {})
    
    def get_user_name(self, user_id: int) -> str:
        return self.get_user_info(user_id).get('name', '')
    
    def get_user_list(self) -> list:
        return list(self._data_dictonary.keys())

    def save_dictionary(self):
        self._data_shelf['user_data'] = self._data_dictonary
        with open('data/data.txt', 'w') as file:
            json.dump(self._data_dictonary, file, indent=2)

    def load_dictionary(self):
        if os.path.exists('data.txt'):
            with open('data.txt', 'r') as file:
                tmp_dictonary = json.load(file)
                self._data_dictonary = {int(key): value for key, value in tmp_dictonary.items()}
                # os.remove('data.txt')
            return

        if not os.path.exists('data/data.txt'):
            if 'user_data' not in self._data_shelf:
                self._data_dictonary = {}
            else:
                self._data_dictonary = dict(self._data_shelf['user_data'])
            return
        with open('data/data.txt', 'r') as file:
            tmp_dictonary = json.load(file)
            self._data_dictonary = {int(key): value for key, value in tmp_dictonary.items()}

data_register = DataRegister()
