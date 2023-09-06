from typing import Any, List, Union

from constants import Action, WrongInputException, WrongInputText


class CustomDataBase:
    """
        Класс - простейшая база данных. Предназначена для хранения и манипуляций с простейшими данными.
        >>>database = CustomDataBase()
        >>>database.set('A', '5')
        >>>database.get('A')
        '5'
        Больше примеров использования можно найти в модуле tests.py
        """



    def __init__(self) -> None:
        self.database = {}
        self.transaction_stack = []

    def get(self, key: str) -> Any:
        if key in self.database:
            return self.database[key]
        else:
            raise WrongInputException(Action.GET, key=key, message=WrongInputText.NULL.value)

    def set(self, key: str, value: str) -> None:
        self.database[key] = value

    def unset(self, key: str) -> None:
        if key in self.database:
            del self.database[key]
        else:
            raise WrongInputException(Action.UNSET, key=key,
                                      message=f"Ошибка: Аргумент {key} отсутствует в базе данных.")

    def counts(self, value: Any) -> int:
        return sum([1 for v in self.database.values() if v == value])

    def find(self, value: Any) -> List[str]:
        return [k for k, v in self.database.items() if v == value]

    def begin_transaction(self) -> None:
        self.transaction_stack.append(self.database.copy())

    def rollback_transaction(self) -> None:
        if self.transaction_stack:
            self.database = self.transaction_stack.pop()
        else:
            raise WrongInputException(Action.ROLLBACK, message=WrongInputText.NO_TRANSACTIONS_TO_ROLLBACK.value)

    def commit_transaction(self) -> None:
        if self.transaction_stack:
            self.transaction_stack.pop()
        else:
            raise WrongInputException(Action.COMMIT, message=WrongInputText.NO_TRANSACTIONS_TO_COMMIT.value)


    def execute_command(self, command, key=None, value=None) -> Union[str, int, None]:

        if command is Action.SET:
            self.set(key, value)
            return
        elif command is Action.GET:
            return self.get(key)
        elif command is Action.UNSET:
            self.unset(key)
            return
        elif command is Action.COUNTS:
            return self.counts(value)
        elif command is Action.FIND:
            return " ".join(key for key in self.find(value))
        elif command is Action.BEGIN:
            self.begin_transaction()
            return
        elif command is Action.ROLLBACK:
            self.rollback_transaction()
            return
        elif command is Action.COMMIT:
            self.commit_transaction()
            return

        raise WrongInputException(message=WrongInputText.WRONG_INPUT_FORMAT.value)
