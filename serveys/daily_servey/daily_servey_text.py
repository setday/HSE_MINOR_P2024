from datetime import time

from utils.timer import make_readable_time

text_cancel_servey = 'Отменить опрос'
text_restart_servey = 'Начать опрос снова'

text_daily_servey_cancelled = 'Опрос отменен. Увидимся позже!👋'
text_lets_begin_daily_servey = 'Перейдем к ежедневному опросу.'
text_thanks_for_answers = 'Спасибо за прохождение опроса!\nОтправил все данные на анализ. В течение недели я напишу тебе, чтобы проверить твое состояние.\nДо встречи!👋'

text_question = [
    '📍 Вопрос 1: Были ли у тебя проявления ОКР (компульсии, обсессии) за последние 5 часов?',
    '📍 Вопрос 2: Какие эмоции ты испытал во время приступа?',
    '📍 Вопрос 3: Что стало триггером для приступа?',
    '📍 Вопрос 4: Оцени тяжесть последствий приступа от 1 до 10.\n(1 - минимальный уровень, 10 - максимальный)',
    '📍 Вопрос 5: Что помогло тебе справиться?',
]

def format_question_and_answer(question: str, answer: str, question_time: time = time(), answer_time: time = time()) -> str:
    if not answer:
        return f'Q: {question}\nA: Нет ответа\n\n'
    return f'Q ({make_readable_time(question_time)}): {question}\nA ({make_readable_time(answer_time)}): {answer}\n\n'

def format_user_data(user_data: dict) -> str:
    res = f'Новая анкета (дневная) от пользователя '+str(user_data['user_id'])+':\n\n'

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
