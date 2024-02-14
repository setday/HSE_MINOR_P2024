from aiogram.types import Message
from aiogram.filters import BaseFilter

from utils.data_register import data_register as dr

class RegisterFilter(BaseFilter):
    def __init__(self, is_register: bool = True):
        # super().__init__()
        
        self.is_register = is_register

    async def __call__(self, message: Message) -> bool:
        if not message.from_user:
            return False

        ud = dr.get_data(message.from_user.id)
        if ud == None:
            ud = {}
        is_reg = ud['reg'] if 'reg' in ud else False

        if self.is_register:
            return is_reg == True
        return is_reg != True