from constants import Action, WrongInputException, WrongInputText
import logging

logger = logging.getLogger(__name__)

class InputFilter:
    """
    Класс предназначенный для форматирования входящего текста в понятные
    для класса custom_database.CustomDataBase параметры.
    >>>input_filter = InputFilter('SET A 5')
    >>>input_filter.is_valid()
    >>>input_filter.cleaned_data
    {'command': Action.SET,
     'key'    : 'A',
     'value'  : '5', })
    Больше примеров использования можно найти в модуле tests.py
    """

    def __init__(self, input_string):
        self.input_string = input_string
        self.error = None

    def is_valid(self) -> bool:
        """
        Парсинг полученной строки при инициализации, и генерация словаря с
        параметрами (self.cleaned_data), если строка валидна.
        Возвращает True если строка валидна, и False если нет.
        :return bool:
        """
        logging.debug(f'Проверка валидности следующей строки "{self.input_string}"')
        arguments = self.input_string.split()
        structured_command = {
            'command': None,
            'key'    : None,
            'value'  : None,
        }
        if len(arguments) in [1, 2, 3]:
            for action in Action:
                if arguments[0].upper() == action.value:

                    structured_command['command'] = action

                    if len(arguments) == 1:
                        if action in [Action.GET, Action.UNSET,
                                      Action.COUNTS, Action.FIND]:
                            self.error = WrongInputException(action, message=WrongInputText.NO_ARGUMENT_NAME.value)
                        elif action in [Action.SET, ]:
                            self.error = WrongInputException(action, message=WrongInputText.NO_ARGUMENT_NAME.value)

                    elif len(arguments) == 2:
                        if action in [Action.GET, Action.UNSET]:
                            structured_command['key'] = arguments[1]
                        elif action in [Action.COUNTS, Action.FIND]:
                            structured_command['value'] = arguments[1]
                        elif action in [Action.SET, ]:
                            self.error = WrongInputException(action, message=WrongInputText.NO_ARGUMENT_VALUE.value)
                        else:
                            self.error = WrongInputException(action, message=WrongInputText.WRONG_INPUT_FORMAT.value)
                    elif len(arguments) == 3:
                        if action in [Action.SET, ]:
                            structured_command['key'] = arguments[1]
                            structured_command['value'] = arguments[2]
                        else:
                            self.error = WrongInputException(message=WrongInputText.WRONG_INPUT_FORMAT.value)

            if not structured_command['command']:
                self.error = WrongInputException(message=WrongInputText.UNKNOWN_COMMAND.value)
        else:
            self.error = WrongInputException(message=WrongInputText.WRONG_INPUT_FORMAT.value)

        if self.error:
            return False
        else:
            logger.debug(f'Строка валидна.')
            self.cleaned_data = structured_command.copy()
            return True
