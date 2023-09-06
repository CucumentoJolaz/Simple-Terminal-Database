from enum import Enum


class Action(Enum):
    """
    Константы для команд. Для использования в классе custom_database.CustomDataBase
    """
    GET = 'GET'
    SET = 'SET'
    UNSET = 'UNSET'
    COUNTS = 'COUNTS'
    FIND = 'FIND'
    END = 'END'
    BEGIN = 'BEGIN'
    ROLLBACK = 'ROLLBACK'
    COMMIT = 'COMMIT'
    HELP = 'HELP'


class WrongInputException(Exception):
    def __init__(self, action=None, key=None, value=None,
                 message="Неверный ввод. Для вывода документации введите HELP"):
        self.key = key
        self.action = action
        self.value = value
        self.message = message
        super().__init__(self.message)


class WrongInputText(Enum):
    """
    Текстовые сообщения для исключений  WrongInputException
    """
    NO_ARGUMENT_NAME = "Ошибка: Отсутствует аргумент и его значение."
    NO_ARGUMENT_VALUE = "Ошибка: Отсутствует значение аргумента."
    UNKNOWN_COMMAND = "Ошибка: Неизвестная команда. Для получения справки введите HELP"
    WRONG_INPUT_FORMAT = "Ошибка: Неверный формат ввода. Для получения справки введите HELP"
    NULL = "NULL"
    NO_TRANSACTIONS_TO_ROLLBACK = "Ошибка: Нет активных транзакций для отмены."
    NO_TRANSACTIONS_TO_COMMIT = "Ошибка: Нет активных транзакций для коммита."


HELP_TEXT = """
    Данное приложение представляет собой базу данных, способную сохранять аргументы со значениями,
    получать информацию о существующих значениях.
    Есть поддержка транзакций. Работа ведётся только в оперативной памяти, сохранения
    на жёстком диске или в иные форматы данных не предусмотрено.
    Команды:
            SET ARGUMENT VALUE - сохранить значение в базе данных.
            GET ARGUMENT  - получить, ранее сохраненную переменную. Если такой переменной
                            не было сохранено, возвращает NULL.
            UNSET ARGUMENT  - удаление ранее установленной переменной. Если значение не было
                              установлено, не делает ничего.
            COUNTS ARGUMENT - показать сколько раз данные значение встречается в базе данных.
            FIND ARGUMENT - вывести найденные установленные переменные для данного значения.
            END - закрыть приложение.
    Поддержка транзакций:
            BEGIN - начать транзакцию.
            ROLLBACK - откатить текущую (самой внутреннюю) транзакцию
            COMMIT - зафиксировать изменения текущей (самой внутренней) транзакции"""
