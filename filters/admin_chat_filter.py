from aiogram.types import Message
from aiogram.filters import BaseFilter

# back_chat_id = -4126577992 # Test
back_chat_id = -1002086532375 # Prod

class AdminChatFilter(BaseFilter):
    def __init__(self, is_this_admin_chat: bool):
        # super().__init__()
        
        self.is_this_feedback = is_this_admin_chat

    async def __call__(self, message: Message) -> bool:
        if self.is_this_feedback:
            return message.chat.id == back_chat_id
        return message.chat.id != back_chat_id