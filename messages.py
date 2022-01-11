


help_message = '''
Через даний телеграм-бот можна придбати потрібний вам одяг чи взуття, вибрати спосіб доставки товару та оплатити його.
'''

start_message = 'Перейдемо до оплати!\n' + help_message

pre_buy_demo_alert = '''\
Введіть номер карти`4242 4242 4242 4242`, оскільки це демонстраційний бот
Рахунок:
'''

terms = '''\
допомога
'''

tm_title = 'Самая настоящая Машина Времени'

tm_description = '''\
Хотите познакомиться со своими пра-пра-пра-пра-бабушкой и дедушкой?
Сделать состояние на ставках?
Пожать руку Хаммурапи и прогуляться по Висячим садам Семирамиды?
Закажите Машину Времени у нас прямо сейчас!
'''

AU_error = '''\
На жаль, ми не можемо відправити товар в цю країну!
'''

wrong_email = '''\
Здається, вказана електронна адреса не дійсна.
Спробуйте ще раз:
'''

successful_payment = '''
Платіж на суму `{total_amount} {currency}` проведений успішно!
'''


MESSAGES = {
    'start': start_message,
    'help': help_message,
    'pre_buy_demo_alert': pre_buy_demo_alert,
    'terms': terms,
    'tm_title': tm_title,
    'tm_description': tm_description,
    'AU_error': AU_error,
    'wrong_email': wrong_email,
    'successful_payment': successful_payment,
}