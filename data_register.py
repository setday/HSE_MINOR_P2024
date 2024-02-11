import json

class DataRegister:
    def __init__(self) -> None:
        self.data_dictonary = {}

    def register_data(self, user_id, data, data_type):
        if user_id not in self.data_dictonary:
            self.data_dictonary[user_id] = {}

        self.data_dictonary[user_id][data_type] = data

    def get_data(self, user_id):
        return self.data_dictonary[user_id]
    
    def get_all_data(self):
        return self.data_dictonary

    def merge_data(self, user_id, data, data_type):
        if user_id not in self.data_dictonary:
            self.data_dictonary[user_id] = {}

        if data_type not in self.data_dictonary[user_id]:
            self.data_dictonary[user_id][data_type] = []

        self.data_dictonary[user_id][data_type].append(data)

    def save_dictionary(self):
        with open('data.txt', 'w') as file:
            json.dump(self.data_dictonary, file, indent=2)

    def load_dictionary(self):
        with open('data.txt', 'r') as file:
            self.data_dictonary = json.load(file)

data_register = DataRegister()
