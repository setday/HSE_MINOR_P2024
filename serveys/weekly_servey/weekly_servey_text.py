from utils.service_text import get_readable_time

text_cancel_servey = 'Отменить опрос'
text_restart_servey = 'Начать опрос снова'

text_weekly_servey_cancelled = 'Опрос отменен.'
text_lets_begin_weekly_servey = 'Перейдем к еженедельному опросу.'
text_thanks_for_answers = 'Спасибо за прохождение опроса!\nОтправил все данные на анализ. В течение недели я напишу тебе, чтобы проверить твое состояние.\nДо встречи!👋'

text_question_1 = '📍 Вопрос 1: Подскажи, замечал ли ты какие-либо закономерности в своих навязчивых идеях или компульсиях на этой неделе?'
text_question_2 = '📍 Вопрос 2: Хорошо! А какие стратегии помогли тебе справиться с симптомами ОКР в период этой недели?'
text_question_3 = '📍 Вопрос 3: Отлично! А с чем был связан твой последний приступ ОКП?'
text_question_4 = '📍 Вопрос 4: Понял! Оцени тяжесть последствий приступа от 1 до 10.'
text_question_5 = '📍 Вопрос 5: Какие эмоции ты испытал во время приступа?'
text_question_6 = '📍 Вопрос 6: Повлиял ли приступ на твой день, на психоэмоциональное состояние?'

def format_question_and_answer(question: str, answer: str, question_time: float = 0, answer_time: float = 0) -> str:
    if not answer:
        return f'Q: {question}\nA: Нет ответа\n\n'
    return f'Q ({get_readable_time(question_time)}): {question}\nA ({get_readable_time(answer_time)}): {answer}\n\n'

def format_user_data(user_data: dict) -> str:
    res = f'Новая анкета (недельная) от пользователя '+str(user_data['user_id'])+':\n\n'

    for i in range(1, 6):
        question_key = f'q{i}'
        answer_key = f'a{i}'
        if question_key in user_data and user_data[question_key]:
            res += format_question_and_answer(
                user_data[question_key]['question'],
                user_data[answer_key]['answer'] if answer_key in user_data and user_data[answer_key] else 'Нет ответа',
                user_data[question_key]['question_time'],
                user_data[answer_key]['answer_time'] if answer_key in user_data and user_data[answer_key] else 0
            )

    return res
