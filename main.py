from constants import Action, WrongInputException, HELP_TEXT
from custom_database import CustomDataBase
from input_filter import InputFilter


def main():
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
                    print(result)

            else:
                raise input_filter.error

        except WrongInputException as e:
            print(e)



if __name__ == '__main__':
    main()
