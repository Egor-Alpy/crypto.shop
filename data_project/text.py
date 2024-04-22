USDT_CONTRACT_ADDRESS = '0xdAC17F958D2ee523a2206206994597C13D831ec7'
RECEIVER = '0xE854c681D8c84e52E125Ac79458A2Acd3ab06aC8'.lower()  # const |||||||||||| .lower() ????????

CANCEL_CMDS = ['start', 'menu', 'addsoft', 'addpartner', 'delsoft', 'delpartner', 'cancel', 'addpromo', 'delpromo']


RUS = 'RUS'

MSG = {
    RUS: {
        'START': '*Здравствуйте! Нажмите на /menu, чтобы начать работу с ботом*',
        'MENU': '*Добро пожаловать!*',
        'SOFT_MENU': '*Выберите софт, чтобы узнать более подробную информацию о нем!*',
        'PARTNER': {
            'ADD': {
                'ID': '*Сначала отправь id партнера, которого хочешь добавить*',
                'NAME': '*Теперь введите имя партнера*',
                'PROMO': '*введите промокод партнера*',
                'DISCOUNT': '*введите размер скидки промокода*',
                'QUANTITY': '*введите кол-во промокодов*'
            },
            'DEL': '*Выбери партнера, которого хочешь удалить из базы данных*'
        },
        'SOFT': {
            'ADD': {
                'NAME': '*Сначала отправь название софта, который хочешь добавить*',
                'DESC': '*А теперь отправь описание*',
                'PRICE': '*Теперь отправь цену софта*'
            },
            'DEL': '*Выберите софт, который хотите удалить*'
        },
        'PROMO': {
            'ADD': {
                'NAME': '*Отправьте промокод, который хотите добавить*',
                'DISCOUNT': '*Теперь отправьте скидку, которая будет начисляться при вводе промокода*',
                'QUANTITY': '*Введите кол-во использований этого промокода*'
            },
            'DEL': 'Выберите промокод, который хотите удалить'
        },
        'ERROR': {
            'INCORRECT_INPUT': '_Некорректный ввод, введите число!_',
            'NO_ROOTS': '*У вас нет прав на использование этой команды!*'
        },
        'OTHERWISE': 'ответ на сообщение не по шаблону!',
        'DATA_BASE': '*База данных была обновлена!*'

    }
}
