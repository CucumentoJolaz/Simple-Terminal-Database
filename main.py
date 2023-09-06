import logging

from constants import Action, WrongInputException, HELP_TEXT
from custom_database import CustomDataBase
from input_filter import InputFilter


logging.basicConfig(filename='app.log',
                        filemode='w',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)
logger = logging.getLogger(__name__)

def main():
    """
    Основная функция для обработки логики с предоставлением пользователю простейшего
    интерфейса, фильтрацией команд пользователя, и исполнения этих команд.
    :return:
    """
    database = CustomDataBase()

    while True:
        user_input = input("> ")
        try:
            input_filter = InputFilter(user_input)
            if input_filter.is_valid():
                if input_filter.cleaned_data['command'] is Action.END:
                    print("База данных заканчивает работу.")
                    break
                elif input_filter.cleaned_data['command'] is Action.HELP:
                    print(HELP_TEXT)
                    continue

                result = database.execute_command(**input_filter.cleaned_data)

                if result is not None:
                    logger.info(f"Результат выполненной команды: {result}")
                    print(result)

            else:
                raise input_filter.error

        except WrongInputException as e:
            logger.warning(e)
            print(e)



if __name__ == '__main__':
    main()
