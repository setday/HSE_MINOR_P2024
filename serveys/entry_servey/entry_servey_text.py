text_hint_begin = 'Начнём опрос!'
text_begin = 'Супер! Начинаем.📃'
text_lets_go = 'Поехали!'

text_understand = 'Понял!'
text_writen_down = 'Зафиксировал!'

text_question_1 = '📍 Вопрос 1: Как часто ты сталкиваешься с проявлением ОКР в среднем?'
text_question_2 = '📍 Вопрос 2: Оцените по 10-балльной шкале, как сильно ОКР влияет на твою повседневную жизнь.\n(1 - не влияет, 10 - оказывается определяющим фактором)'

text_lets_begin_workig_together = '📔Зафиксировал! Ну что, начнём вести дневник?'

frequency_answers = {
    '• Несколько раз на дню ': '4',
    '• Один раз в день ': '3',
    '• Один или несколько раз в неделю': '2',
    '• Реже, чем раз в неделю': '1',
}

def format_user_data(user_data: dict) -> str:
    return f'Новый пользователь '+str(user_data['user_id'])+':\n'\
            f'Частота: '+str(user_data['frequency'])+'\n'\
            f'Тяжесть: '+str(user_data['severity'])+'\n'
