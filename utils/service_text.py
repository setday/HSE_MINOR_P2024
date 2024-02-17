from datetime import time

from utils.timer import make_readable_time

text_error_try_again = 'Ошибка! Попробуйте еще раз.'

text_yes = 'Да'
text_no = 'Нет'

def format_question_and_answer(question: str, answer: str, question_time: time = time(), answer_time: time = time()) -> str:
    if not answer:
        return f'Q: {question}\nA: Нет ответа\n\n'
    return f'Q ({make_readable_time(question_time)}): {question}\nA ({make_readable_time(answer_time)}): {answer}\n\n'

def format_user_data(user_data: dict, type: int = 1) -> str: # type 1 - daily, 2 - weekly
    res = f'Новая анкета '
    res += '(дневная)' if type == 1 else '(недельная)'
    res += ' от пользователя '
    res += str(user_data['user_id'])
    res += ' | ('
    # res += user_data['user_name']
    res += '):\n\n'

    for i in range(1, 6):
        question_key = f'q{i}'
        answer_key = f'a{i}'
        if question_key in user_data and user_data[question_key]:
            res += format_question_and_answer(
                user_data[question_key]['question'],
                user_data[answer_key]['answer'] if answer_key in user_data and user_data[answer_key] else 'Нет ответа',
                user_data[question_key]['question_time'],
                user_data[answer_key]['answer_time'] if answer_key in user_data and user_data[answer_key] else time()
            )

    return res
