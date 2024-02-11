import time as t

text_error_try_again = 'Ошибка! Попробуйте еще раз.'

text_yes = 'Да'
text_no = 'Нет'

def get_readable_time(time: float) -> str:
    return t.strftime('%H:%M', t.localtime(time))
